import gi
import os
from configuracion import Configuracion
# Descomentar la linea de abajo para habilitar la captura de pantalla
# from blurcapture import capturar_y_desenfocar_pantalla
from shutil import copy, copytree

gi.require_version('Gtk', '3.0')
gi.require_version('GioUnix', '2.0')
from gi.repository import Gtk, Gdk, GioUnix

APP = "pylogout"
config = f"{APP}.conf"
config_base = {}

cf = Configuracion(APP, config, config_base)
# Descomentar la linea de abajo para habilitar la captura de pantalla
# capturar_y_desenfocar_pantalla(str(cf.get_dir() / "fondo/fondo_borroso.png"), 10)

if os.path.getsize(cf.get_dir() / config) == 0:
    copy('pylogout.conf', cf.get_dir() / config)

fondo_dir = cf.get_dir() / 'fondo'
if not fondo_dir.exists():
    copytree('fondo', fondo_dir)

botones_dir = cf.get_dir() / 'botones'
if not botones_dir.exists():
    copytree('botones', botones_dir)

config_data = cf.read_conf()
config_dir = cf.get_dir()

class ShutdownApp(Gtk.Window):
    def __init__(self, config_data, config_dir):
        Gtk.Window.__init__(self)
        self.config_data = config_data

        self.set_decorated(False)
        self.fullscreen()

        # Usar Gtk.Overlay para superponer la imagen y los botones
        overlay = Gtk.Overlay()
        self.add(overlay)

        # Crear el widget de imagen y agregarlo al overlay
        # La imagen se convierte en el "child" principal del overlay
        try:
            background_path = config_dir / config_data['theme']['background']
            image = Gtk.Image.new_from_file(str(background_path))
            overlay.add(image)  # Usa .add() para el child principal
        except Exception as e:
            print(f"No se pudo cargar la imagen: {e}")
            # Si no se carga la imagen, poner un color de fondo
            fallback_box = Gtk.Box()
            overlay.add(fallback_box)

        # Contenedor para los botones
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.set_valign(Gtk.Align.CENTER)
        
        # Agregar el contenedor de botones como un overlay
        overlay.add_overlay(main_box) # Usar .add_overlay() para los widgets superpuestos

        # Crear los botones como imágenes

        # Botón para apagar
        shutdown_icon_path = config_dir / config_data['theme']['shutdown_icon']
        image_poweroff = Gtk.Image.new_from_file(str(shutdown_icon_path))
        shutdown_btn = Gtk.Button()
        shutdown_btn.set_image(image_poweroff)
        shutdown_btn.connect("clicked", self.on_shutdown_clicked)

        # Botón para reiniciar
        restart_icon_path = config_dir / config_data['theme']['restart_icon']
        image_reboot = Gtk.Image.new_from_file(str(restart_icon_path))
        reboot_btn = Gtk.Button()
        reboot_btn.set_image(image_reboot)
        reboot_btn.connect("clicked", self.on_reboot_clicked)

        # Botón para cerrar sesión
        logout_icon_path = config_dir / config_data['theme']['logout_icon']
        image_logout = Gtk.Image.new_from_file(str(logout_icon_path))
        logout_btn = Gtk.Button()
        logout_btn.set_image(image_logout)
        logout_btn.connect("clicked", self.on_logout_clicked)

        # Botón para hibernar
        hibernate_icon_path = config_dir / config_data['theme']['hibernate_icon']
        image_hibernate = Gtk.Image.new_from_file(str(hibernate_icon_path))
        hibernate_btn = Gtk.Button()
        hibernate_btn.set_image(image_hibernate)
        hibernate_btn.connect("clicked", self.on_hibernate_clicked)

        # Botón para Lock
        # lock_icon_path = config_dir / config_data['theme']['lock_icon']
        # image_lock = Gtk.Image.new_from_file(str(lock_icon_path))
        # lock_btn = Gtk.Button()
        # lock_btn.set_image(image_lock)
        # lock_btn.connect("clicked", self.on_lock_clicked)

        # Botón para Suspend
        # suspend_icon_path = config_dir / config_data['theme']['suspend_icon']
        # image_suspend = Gtk.Image.new_from_file(str(suspend_icon_path))
        # suspend_btn = Gtk.Button()
        # suspend_btn.set_image(image_suspend)
        # suspend_btn.connect("clicked", self.on_suspend_clicked)

        # Botón para Switch
        # switch_icon_path = config_dir / config_data['theme']['switch_icon']
        # image_switch = Gtk.Image.new_from_file(str(switch_icon_path))
        # switch_btn = Gtk.Button()
        # switch_btn.set_image(image_switch)
        # switch_btn.connect("clicked", self.on_switch_clicked)

        # Botón para Cancel
        cancel_icon_path = config_dir / config_data['theme']['cancel_icon']
        image_cancel = Gtk.Image.new_from_file(str(cancel_icon_path))
        cancel_btn = Gtk.Button()
        cancel_btn.set_image(image_cancel)
        cancel_btn.connect("clicked", self.on_cancel_clicked)

        main_box.pack_start(shutdown_btn, True, False, 0)
        main_box.pack_start(reboot_btn, True, False, 0)
        main_box.pack_start(logout_btn, True, False, 0)
        main_box.pack_start(hibernate_btn, True, False, 0)
        # main_box.pack_start(lock_btn, True, False, 0)
        # main_box.pack_start(suspend_btn, True, False, 0)
        # main_box.pack_start(switch_btn, True, False, 0)
        main_box.pack_start(cancel_btn, True, False, 0)

        self.connect("key-press-event", self.on_key_press)

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            print("Saliendo con la tecla ESC...")
            Gtk.main_quit()
        # Aqui se pondria las teclas rapidas cuando se implementen
        if event.keyval == Gdk.KEY_s:
            self.on_shutdown_clicked(widget)
            Gtk.main_quit()

    def on_shutdown_clicked(self, widget):
        print("Apagando...")
        command = self.config_data['commands']['shutdown']
        os.system(command)
        Gtk.main_quit()
        
    def on_reboot_clicked(self, widget):
        print("Reiniciando...")
        command = self.config_data['commands']['restart']
        os.system(command)
        Gtk.main_quit()
        
    def on_logout_clicked(self, widget):
        print("Cerrando sesión...")
        command = self.config_data['commands']['logout']
        os.system(command)
        Gtk.main_quit()

    def on_hibernate_clicked(self, widget):
        print("Hibernando...")
        command = self.config_data['commands']['hibernate']
        os.system(command)
        Gtk.main_quit()

    # def on_lock_clicked(self, widget):
    #     print("Bloqueando...")
    #     command = self.config_data['commands']['lock']
    #     os.system(command)
    #     Gtk.main_quit()

    # def on_suspend_clicked(self, widget):
    #     print("Suspenciendo...")
    #     command = self.config_data['commands']['suspend']
    #     os.system(command)
    #     Gtk.main_quit()

    # def on_switch_clicked(self, widget):
    #     print("Cambiando de Usuario...")
    #     command = self.config_data['commands']['switch']
    #     os.system(command)
    #     Gtk.main_quit()

    def on_cancel_clicked(self, widget):
        print("Saliendo...")
        Gtk.main_quit()
 

win = ShutdownApp(config_data, config_dir)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
