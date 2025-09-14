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
        self.config_dir = config_dir

        # --- Implementación de Atajos de Teclado ---
        # 1. Mapear nombres de acción a funciones
        self.action_map = {
            'shutdown': self.on_shutdown_clicked,
            'restart': self.on_reboot_clicked,
            'logout': self.on_logout_clicked,
            'hibernate': self.on_hibernate_clicked,
            'cancel': self.on_cancel_clicked,
            'lock': self.on_lock_clicked,
            'suspend': self.on_suspend_clicked,
            'switch': self.on_switch_clicked,
        }

        # 2. Crear el diccionario invertido de Tecla -> Acción
        self.key_map = {v: k for k, v in self.config_data['shortcuts'].items()}
        # -----------------------------------------

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
            overlay.add(Gtk.Box())

        # Contenedor para los botones
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
        main_box.set_halign(Gtk.Align.CENTER)
        main_box.set_valign(Gtk.Align.CENTER)
        
        # Agregar el contenedor de botones como un overlay
        overlay.add_overlay(main_box) # Usar .add_overlay() para los widgets superpuestos

        # --- Crear botones dinámicamente ---
        # Lee el orden y la presencia de los botones desde el archivo de configuración
        button_order = self.config_data['layout']['buttons']
        
        for action_key in button_order:
            # Solo crea el widget si la acción está definida en el action_map
            if action_key in self.action_map:
                widget = self._create_button_with_label(action_key)
                if widget:
                    main_box.pack_start(widget, True, False, 0)

        self.connect("key-press-event", self.on_key_press)

    def _create_button_with_label(self, action_key):
        """Crea una VBox que contiene un botón con imagen y una etiqueta con formato."""
        try:
            # 1. Obtener datos de la configuración
            label_text = self.config_data['labels'][action_key]
            shortcut_key = self.config_data['shortcuts'][action_key]
            icon_name = self.config_data['theme'][f'{action_key}_icon']
            icon_path = self.config_dir / icon_name
            color = self.config_data['theme']['highlight_color']

            # 2. Construir el marcado Pango para la etiqueta
            pos = label_text.lower().find(shortcut_key.lower())
            if pos != -1:
                # Resaltar la primera ocurrencia de la letra en el texto
                pre = label_text[:pos]
                char = label_text[pos:pos+len(shortcut_key)]
                post = label_text[pos+len(shortcut_key):]
                markup = f"{pre}<span foreground='{color}'>{char}</span>{post}"
            else:
                # Añadir el atajo entre paréntesis al final
                markup = f"{label_text} (<span foreground='{color}'>{shortcut_key}</span>)"

            # 3. Crear los widgets
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

            # Botón con imagen
            image = Gtk.Image.new_from_file(str(icon_path))
            button = Gtk.Button()
            button.set_image(image)
            button.connect("clicked", self.action_map[action_key])
            vbox.pack_start(button, False, False, 0)

            # Etiqueta con formato
            label = Gtk.Label()
            label.set_use_markup(True)
            label.set_markup(markup)
            vbox.pack_start(label, False, False, 0)

            return vbox
        except KeyError as e:
            print(f"Advertencia: Falta la configuración para la acción '{action_key}': {e}. No se creará el botón.")
            return None

    def on_key_press(self, widget, event):
        # Obtener el nombre de la tecla presionada
        key_name = Gdk.keyval_name(event.keyval)

        # Comprobar si la tecla está en el mapa de atajos
        if key_name in self.key_map:
            # Obtener el nombre de la acción (ej: 'shutdown')
            action_name = self.key_map[key_name]
            
            # Comprobar si esa acción tiene una función asociada
            if action_name in self.action_map:
                print(f"Atajo de teclado detectado: '{key_name}' -> Acción: '{action_name}'")
                # Obtener y ejecutar la función (pasamos None como argumento del widget)
                self.action_map[action_name](None)

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

    def on_lock_clicked(self, widget):
        print("Bloqueando...")
        command = self.config_data['commands']['lock']
        os.system(command)
        Gtk.main_quit()

    def on_suspend_clicked(self, widget):
        print("Suspenciendo...")
        command = self.config_data['commands']['suspend']
        os.system(command)
        Gtk.main_quit()

    def on_switch_clicked(self, widget):
        print("Cambiando de Usuario...")
        command = self.config_data['commands']['switch']
        os.system(command)
        Gtk.main_quit()

    def on_cancel_clicked(self, widget):
        print("Saliendo...")
        Gtk.main_quit()
 

win = ShutdownApp(config_data, config_dir)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
