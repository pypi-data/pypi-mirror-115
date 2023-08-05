
import gettext
import sys
import os
import subprocess
import locale
import time

from gi import require_version


require_version("Gtk", "3.0")
require_version("Gdk", "3.0")

from gi.repository import Gtk, Gio, Gdk

from nvidia_fan_control import __author__, __version__, __website_url__
from nvidia_fan_control.settings import settings


# sys.path.append(os.path.abspath("."))
sys.path.insert(0, os.path.abspath("."))


def _init_style():
    """Load the application's CSS file"""

    screen = Gdk.Screen.get_default()
    provider = Gtk.CssProvider()
    add_provider = Gtk.StyleContext.add_provider_for_screen
    css_path = os.path.join(os.path.dirname(__file__), 'font.css')
    # css_path = './font.css'
    provider.load_from_file(Gio.file_new_for_path(css_path))
    add_provider(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


# Translations related
# os.environ['LANGUAGE'] = 'en'  # TODO to remove, used for translations testing
locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain('nvidiafancontrol', os.path.join(os.path.dirname(__file__), '../share/locale'))
gettext.textdomain('nvidiafancontrol')
# ln = gettext.translation('nvidiafancontrol', localedir='/usr/share/locale', fallback=True)
gettext.install('nvidiafancontrol', os.path.join(os.path.dirname(__file__), '../share/locale'))
_ = gettext.gettext
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '../share/locale')))


# constants
TITLE = _("Nvidia Fan control")
APP_ID = "com.github.tudo75.nvidia-fan-control"


class NvidiaFanControl(Gtk.Application):
    """
    Main Class
    """

    def _init__(self):
        print("APP start init")
        super(NvidiaFanControl, self).__init__(application_id=APP_ID)
        self.set_flags(Gio.ApplicationFlags.UNIQUE)
        self.connect("activate", self.do_activate)
        self.connect("destroy", self.do_shutdown)
        self.window = None
        self.main_panel = None
        self.toolbar = None
        self.header_bar = None

    def do_activate(self):
        """Activate method required
        """
        self._init_widgets()
        self._create_window_structure()
        _init_style()
        self.add_window(self.window)
        self.window.show_all()

    def do_shutdown(self):
        """Callback when app is closed
        """
        Gtk.Application.do_shutdown(self)
        sys.exit()

    def _init_widgets(self):
        """Initialize widgets
        """
        self.window = Gtk.Window()
        self.header_bar = Gtk.HeaderBar()
        self.main_panel = Gtk.Label()
        self.main_panel.set_name("main_panel")
        self.toolbar = Gtk.Grid()

    def _create_window_structure(self):
        """Generate the Gui structure"""

        self.header_bar.set_title(TITLE)
        self.header_bar.set_has_subtitle(False)
        self.header_bar.set_show_close_button(True)

        hbox_about_btn = Gtk.HBox(spacing=6)
        hbox_about_btn.pack_start(
            Gtk.Image.new_from_icon_name('nvidiafancontrol', Gtk.IconSize.DND),
            True,
            True,
            0
        )
        hbox_about_btn.pack_start(Gtk.Label(_("About us")), True, True, 0)
        about_btn = Gtk.Button()
        about_btn.add(hbox_about_btn)
        about_btn.connect("clicked", self.on_about)
        self.header_bar.pack_start(about_btn)

        self.window.set_titlebar(self.header_bar)

        scroll_win = Gtk.ScrolledWindow()
        self.refresh_smi()
        self.main_panel.set_vexpand(True)
        scroll_win.add(self.main_panel)

        # Toolbar buttons
        hbox_xconfig_btn = Gtk.HBox(spacing=6)
        hbox_xconfig_btn.pack_start(
            Gtk.Image.new_from_icon_name('emblem-system-symbolic', Gtk.IconSize.LARGE_TOOLBAR),
            True,
            True,
            0
        )
        hbox_xconfig_btn.pack_start(Gtk.Label(_("Initialize Nvidia Xconfig")), True, True, 0)
        self.xconfig_btn = Gtk.Button()
        self.xconfig_btn.add(hbox_xconfig_btn)
        self.xconfig_btn.connect("clicked", self.set_config)
        if settings.get_boolean('initialized'):
            self.xconfig_btn.set_sensitive(False)

        hbox_reboot_btn = Gtk.HBox(spacing=6)
        hbox_reboot_btn.pack_start(
            Gtk.Image.new_from_icon_name('system-reboot-symbolic', Gtk.IconSize.LARGE_TOOLBAR),
            True,
            True,
            0
        )
        hbox_reboot_btn.pack_start(Gtk.Label(_("Reboot the system")), True, True, 0)
        self.reboot_btn = Gtk.Button()
        self.reboot_btn.add(hbox_reboot_btn)
        self.reboot_btn.connect("clicked", self.reboot)
        self.reboot_btn.set_sensitive(False)

        speed_lbl = Gtk.Label(_("Set fan speed %"))

        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
        self.scale.set_hexpand(True)
        self.scale.set_digits(0)
        self.scale.add_mark(0, Gtk.PositionType.TOP, "0")
        self.scale.add_mark(100, Gtk.PositionType.TOP, "100")
        self.scale.set_value(self.get_fan_speed())

        hbox_set_speed_btn = Gtk.HBox(spacing=6)
        hbox_set_speed_btn.pack_start(
            Gtk.Image.new_from_icon_name('document-save-symbolic', Gtk.IconSize.LARGE_TOOLBAR),
            True,
            True,
            0
        )
        hbox_set_speed_btn.pack_start(Gtk.Label(_("Set speed")), True, True, 0)
        set_speed_btn = Gtk.Button()
        set_speed_btn.add(hbox_set_speed_btn)
        set_speed_btn.connect('clicked', self.set_speed)

        self.toolbar.set_column_spacing(15)
        self.toolbar.set_row_spacing(5)
        self.toolbar.set_margin_left(10)
        self.toolbar.set_margin_top(10)
        self.toolbar.set_margin_right(10)
        self.toolbar.set_margin_bottom(10)
        self.toolbar.set_column_homogeneous(True)
        self.toolbar.set_row_homogeneous(False)
        self.toolbar.attach(self.xconfig_btn, 0, 0, 2, 1)
        self.toolbar.attach(self.reboot_btn, 2, 0, 2, 1)
        self.toolbar.attach(speed_lbl, 0, 1, 1, 1)
        self.toolbar.attach(self.scale, 1, 1, 2, 1)
        self.toolbar.attach(set_speed_btn, 3, 1, 1, 1)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(False)
        grid.attach(scroll_win, 0, 0, 2, 1)
        grid.attach(self.toolbar, 0, 1, 2, 1)
        grid.set_vexpand(True)

        self.window.add(grid)

        geometry = settings.get_integer_list("geometry")
        self.window.resize(geometry[0], geometry[1])
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_icon_name('nvidiafancontrol')
        self.window.set_default_icon_name('nvidiafancontrol')

    def on_about(self, button):
        """Create and display an about us dialog window

        Args:
            button: button who trigger the open action

        Returns:
            a modal about dialog
        """
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True, decorated=True, use_header_bar=True)
        about_dialog.connect("response", self.on_close)

        about_dialog.set_logo_icon_name('nvidiafancontrol')
        # about_dialog.set_logo(Pixbuf.new_from_file_at_scale(LOGO_PATH, 128, 128, True))
        about_dialog.set_authors([__author__])
        about_dialog.set_program_name(TITLE)
        about_dialog.set_version(__version__)
        about_dialog.set_comments(_('\nGUI fan controller for nvidia \nNote: Tested on RTX 3060\n'))
        about_dialog.set_website(__website_url__)
        about_dialog.set_website_label(_("Github Code Repository"))

        about_dialog.set_documenters([__author__])
        about_dialog.set_translator_credits(_("translator-credits"))
        about_dialog.add_credit_section(
            'nvidia-fan-control-gui-linux',
            ['https://github.com/dcostersabin/nvidia-fan-control-gui-linux']
        )
        about_dialog.set_copyright("NVIDIA is a registered trademark of NVIDIA Corporation.\n"
                                   "This app and it's creator are not related to NVIDIA")

        about_dialog.set_license_type(Gtk.License.GPL_3_0_ONLY)

        # hack to remove doubled buttons
        hbar = about_dialog.get_header_bar()
        for child in hbar.get_children():
            if type(child) in [Gtk.Button, Gtk.ToggleButton]:
                child.destroy()

        # show the about dialog
        about_dialog.run()
        about_dialog.destroy()

    @staticmethod
    def on_close(action, parameter):
        """ Action to be taken on about dialog close event

        Args:
            action: close action of the about dialog
            parameter: unused value
        """
        action.destroy()

    def refresh_smi(self):
        """Fetch nvidia-smi results and display results in the main_panel"""

        try:
            smi_result = subprocess.check_output('nvidia-smi', shell=True, universal_newlines=True)
            self.main_panel.set_text(smi_result)
        except subprocess.SubprocessError as error:
            # nvidia-smi not found
            msg = _("Can't fetch data.\nPlease install nvidia-smi!")
            self.main_panel.set_text(msg)
            self.error_dialog(msg)

    def get_fan_speed(self):
        """Fetch nvidia-smi results for fan speed

        Returns:
            fan speed percent as int value

        """

        try:
            cmd = "nvidia-smi --query-gpu=fan.speed --format=csv,noheader,nounits"
            fan_speed = subprocess.check_output(cmd, shell=True, universal_newlines=True)
            return int(fan_speed)
        except subprocess.SubprocessError as error:
            # nvidia-smi not found
            return 0

    # setting the overall configurations
    def set_config(self, button):
        try:
            # checking if nvidia-smi is installed
            subprocess.check_output('nvidia-smi', shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            try:
                # allowing the gpu to overclock manually
                subprocess.check_output('pkexec nvidia-xconfig -a --cool-bits=28 --allow-empty-initial-configuration',
                                        shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                # success message
                self.info_dialog(self, _('Success! New X configuration file written to /etc/X11/xorg.conf'))
                # update initialized key to keep track
                settings.set_boolean('initialized', True)
                # enable reboot button
                self.reboot_btn.set_sensitive(True)
                # disable xconfig button
                self.xconfig_btn.set_sensitive(False)

            except subprocess.SubprocessError as error:
                # If xconfig failed to init
                self.error_dialog(str(error.stdout))
        except subprocess.SubprocessError as error:
            # nvidia-smi not found
            self.error_dialog(str(error.stdout) + _("\n\nPlease install it!"))

    def reboot(self, widget):
        result = self.confirm_dialog(self, title=_('Reboot'), msg=_('Do you want to reboot?'), explain_msg="")
        if result == Gtk.ResponseType.YES:
            subprocess.check_output('pkexec reboot', shell=True, universal_newlines=True)
        else:
            self.error_dialog(_('Reboot is required to implement the changes'))

    def set_speed(self, widget):
        val = int(self.scale.get_value())
        try:
            # set the gpu for over clock
            command = "nvidia-settings -a '[gpu:0]/GPUFanControlState=1'"
            subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            # command to set the speed
            command = "nvidia-settings -a '[fan]/GPUTargetFanSpeed=" + str(val) + "'"
            # running a subprocess
            subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            # sleep to coordinate with nvidia-smi
            time.sleep(8.0)
            self.info_dialog(self, _("Fan Speed Set To ") + str(val))
            self.refresh_smi()
        except subprocess.SubprocessError as error:
            # failed to set the value
            self.error_dialog(str(error.stdout) + _("\n\nFailed To Set Fan Speed"))

    def info_dialog(self, widget, message):
        md = Gtk.MessageDialog(self.window,
                               Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.INFO,
                               Gtk.ButtonsType.CLOSE, message)

        h_bar = Gtk.HeaderBar()
        # h_bar.set_title("Error")
        h_bar.set_show_close_button(True)
        md.set_titlebar(h_bar)
        md.show_all()

        md.run()
        md.destroy()

    def confirm_dialog(self, widget, title, msg, explain_msg):
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=msg,
            title=title
        )
        dialog.format_secondary_text(explain_msg)
        response = dialog.run()
        dialog.destroy()
        return response

    def error_dialog(self, message, running_tests=False):
        """Show a GTK Error Pop Up with message.

        Args:
            message: The message to display.
            running_tests: If True running from testsuite. Do not show popup.
        """
        # Always print the error message first
        print("\033[91mError:\033[0m", message)
        # Then display a Gtk Popup
        popup = Gtk.Dialog(title=_("Error"), transient_for=Gtk.Window())
        popup.set_default_size(settings.get_integer_list("geometry")[0] - 60, 1)
        popup.add_button(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)

        h_bar = Gtk.HeaderBar()
        h_bar.set_title(_("Error"))
        h_bar.set_show_close_button(True)
        popup.set_titlebar(h_bar)

        message_label = Gtk.Label()
        message_label.set_hexpand(True)
        message_label.set_line_wrap(True)
        message_label.set_size_request(settings.get_integer_list("geometry")[0] - 140, 1)
        message_label.set_text(message)
        box = popup.get_child()
        box.set_border_width(12)
        grid = Gtk.Grid()
        grid.set_column_spacing(12)
        box.pack_start(grid, False, False, 0)
        error_icon = Gtk.Image.new_from_icon_name('dialog-error', Gtk.IconSize.DIALOG)
        grid.attach(error_icon, 0, 0, 1, 1)
        grid.attach(message_label, 1, 0, 1, 1)
        popup.show_all()
        if not running_tests:
            popup.run()
            popup.destroy()
