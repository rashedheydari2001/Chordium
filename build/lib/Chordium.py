# pyright: reportMissingModuleSource=false
# pyright: reportUnknownMemberType=false
# reportUnknownArgumentType=false

from __future__ import annotations

import sys
from typing import cast, override

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gst", "1.0")

from gi.repository import Gio, GLib, GObject, Gst, Gtk  # type: ignore[import-untyped]

Gst.init(None)


class TrackItem(GObject.Object):
    """Data model representing a single track in the playlist."""

    def __init__(self, name: str, uri: str) -> None:
        super().__init__()
        self.name: str = name
        self.uri: str = uri


class MusicPlayerWindow(Gtk.ApplicationWindow):
    label_title: Gtk.Label
    player: Gst.Element
    btn_play: Gtk.Button
    volume_scale: Gtk.Scale
    is_playing: bool
    playlist: Gio.ListStore[TrackItem]
    list_view: Gtk.ListView
    current_index: int

    def __init__(self, app: Gtk.Application) -> None:
        super().__init__(
            application=app,
            title="Python GTK4 Player",
            default_width=600,
            default_height=500,
        )

        self.is_playing = False
        self.current_index = -1

        # GStreamer Engine Setup
        element = Gst.ElementFactory.make("playbin", "player")
        if element is None:
            print("Error: Could not create GStreamer playbin element.")
            sys.exit(1)
        self.player = element

        # Audio Bus Listener for Next Track (EOS)
        bus = self.player.get_bus()
        if bus is not None:
            _ = bus.add_signal_watch()
            _ = bus.connect("message::eos", self.on_eos)

        # Playlist Data Store
        self.playlist = cast(Gio.ListStore[TrackItem], Gio.ListStore.new(TrackItem))

        # UI Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main_box.set_margin_top(16)
        main_box.set_margin_bottom(16)
        main_box.set_margin_start(16)
        main_box.set_margin_end(16)
        self.set_child(main_box)

        # Title Display Label
        self.label_title = Gtk.Label(label="No track playing")
        self.label_title.add_css_class("title-2")
        main_box.append(self.label_title)

        # Controls Container Box
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        controls_box.set_halign(Gtk.Align.CENTER)
        main_box.append(controls_box)

        btn_open_file = Gtk.Button(label="Open File")
        _ = btn_open_file.connect("clicked", self.on_open_file_clicked)
        controls_box.append(btn_open_file)

        btn_open_folder = Gtk.Button(label="Open Folder")
        _ = btn_open_folder.connect("clicked", self.on_open_folder_clicked)
        controls_box.append(btn_open_folder)

        self.btn_play = Gtk.Button(label="Play")
        _ = self.btn_play.connect("clicked", self.on_play_pause_clicked)
        self.btn_play.set_sensitive(False)
        controls_box.append(self.btn_play)

        btn_next = Gtk.Button(label="Next")
        _ = btn_next.connect("clicked", self.on_next_clicked)
        controls_box.append(btn_next)

        # Volume Slider
        volume_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        volume_label = Gtk.Label(label="Volume:")
        self.volume_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL, 0.0, 1.0, 0.05
        )
        self.volume_scale.set_value(0.8)
        self.volume_scale.set_hexpand(True)
        _ = self.volume_scale.connect("value-changed", self.on_volume_changed)

        volume_box.append(volume_label)
        volume_box.append(self.volume_scale)
        main_box.append(volume_box)

        # Playlist View (GTK4 ListView)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)

        selection_model = Gtk.SingleSelection.new(self.playlist)
        factory = Gtk.SignalListItemFactory()
        _ = factory.connect("setup", self.setup_playlist_item)
        _ = factory.connect("bind", self.bind_playlist_item)

        self.list_view = Gtk.ListView.new(selection_model, factory)
        _ = self.list_view.connect("activate", self.on_item_activated)

        scrolled_window.set_child(self.list_view)
        main_box.append(scrolled_window)

    # --- UI & Playlist Callbacks ---

    def setup_playlist_item(
        self, _factory: Gtk.SignalListItemFactory, item: Gtk.ListItem
    ) -> None:
        label = Gtk.Label(xalign=0)
        label.set_margin_start(8)
        item.set_child(label)

    def bind_playlist_item(
        self, _factory: Gtk.SignalListItemFactory, item: Gtk.ListItem
    ) -> None:
        obj: GObject.Object | None = item.get_item()
        label = item.get_child()
        if isinstance(obj, TrackItem) and isinstance(label, Gtk.Label):
            label.set_text(obj.name)

    def on_item_activated(self, _list_view: Gtk.ListView, position: int) -> None:
        self.play_track_at_index(position)

    # --- File / Folder Selection ---

    def on_open_file_clicked(self, _button: Gtk.Button) -> None:
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Audio File")

        audio_filter = Gtk.FileFilter()
        audio_filter.set_name("Audio Files")
        audio_filter.add_mime_type("audio/*")

        filters = cast(Gio.ListStore[Gtk.FileFilter], Gio.ListStore.new(Gtk.FileFilter))
        filters.append(audio_filter)
        dialog.set_filters(filters)

        dialog.open(self, None, self.on_file_selected)

    def on_file_selected(self, dialog: Gtk.FileDialog, result: Gio.AsyncResult) -> None:
        try:
            file: Gio.File | None = dialog.open_finish(result)
            if file:
                basename = file.get_basename() or "Unknown Track"
                track = TrackItem(basename, file.get_uri())
                self.playlist.append(track)
                if self.current_index == -1:
                    self.play_track_at_index(0)
        except GLib.Error as err:
            print(f"Error opening file: {err.message}")

    def on_open_folder_clicked(self, _button: Gtk.Button) -> None:
        dialog = Gtk.FileDialog()
        dialog.set_title("Select Music Folder")
        dialog.select_folder(self, None, self.on_folder_selected)

    def on_folder_selected(
        self, dialog: Gtk.FileDialog, result: Gio.AsyncResult
    ) -> None:
        try:
            folder: Gio.File | None = dialog.select_folder_finish(result)
            if folder:
                self.load_audio_files_from_folder(folder)
        except GLib.Error as err:
            print(f"Error selecting folder: {err.message}")

    def load_audio_files_from_folder(self, folder: Gio.File) -> None:
        audio_extensions = (".mp3", ".flac", ".wav", ".ogg", ".m4a")
        enumerator = folder.enumerate_children(
            "standard::*", Gio.FileQueryInfoFlags.NONE, None
        )

        initial_count = self.playlist.get_n_items()

        while True:
            info = enumerator.next_file(None)
            if info is None:
                break
            filename = info.get_name()
            if filename.lower().endswith(audio_extensions):
                child_file = folder.get_child(filename)
                track = TrackItem(filename, child_file.get_uri())
                self.playlist.append(track)

        if self.playlist.get_n_items() > initial_count and self.current_index == -1:
            self.play_track_at_index(0)

    # --- Audio Engine Controls ---

    def play_track_at_index(self, index: int) -> None:
        if index < 0 or index >= self.playlist.get_n_items():
            return

        item: GObject.Object | None = self.playlist.get_item(index)
        if isinstance(item, TrackItem):
            self.current_index = index
            _ = self.player.set_state(Gst.State.NULL)
            self.player.set_property("uri", item.uri)
            _ = self.player.set_state(Gst.State.PLAYING)

            self.label_title.set_text(item.name)
            self.btn_play.set_sensitive(True)
            self.btn_play.set_label("Pause")
            self.is_playing = True

    def on_play_pause_clicked(self, _button: Gtk.Button) -> None:
        if self.is_playing:
            _ = self.player.set_state(Gst.State.PAUSED)
            self.btn_play.set_label("Play")
            self.is_playing = False
        else:
            _ = self.player.set_state(Gst.State.PLAYING)
            self.btn_play.set_label("Pause")
            self.is_playing = True

    def on_next_clicked(self, _button: Gtk.Button) -> None:
        if self.playlist.get_n_items() > 0:
            next_index = (self.current_index + 1) % self.playlist.get_n_items()
            self.play_track_at_index(next_index)

    def on_eos(self, _bus: Gst.Bus, _msg: Gst.Message) -> None:
        """Autoplay next song when stream ends."""
        self.on_next_clicked(self.btn_play)

    def on_volume_changed(self, scale: Gtk.Scale) -> None:
        self.player.set_property("volume", scale.get_value())


class MusicPlayerApp(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(application_id="com.example.MusicPlayer")

    @override
    def do_activate(self) -> None:
        win = self.props.active_window
        if not win:
            win = MusicPlayerWindow(self)
        win.present()


def main() -> None:
    app = MusicPlayerApp()
    _ = app.run(sys.argv)


if __name__ == "__main__":
    main()
