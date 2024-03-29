pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'gabtag')

gnome.compile_resources('gabtag',
  'gabtag.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('APP_ID', app_id)
conf.set('VERSION', meson.project_version())
conf.set('DEVEL', get_option('devel'))
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'gabtag.in',
  output: meson.project_name(),
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

gabtag_sources = [
  '__init__.py',
  'main.py',
  'version.py',

  'exception.py',
  'constant.py',
  'extension_manager.py',
  'dir_manager.py',
  'selection_handler.py',
  'tools.py',
  'model.py',

  'treeview.py',
  'view.py',
  'window_gtk.py',
  'controller.py',
  'event_machine.py',

  'audio_extension_handler.py',
  'audio_getter.py',
  'audio_mp3_file_handler.py',
  'audio_ogg_file_handler.py',

  'crawler_data.py',
  'crawler_directory.py',
  'crawler_modification.py',
]

install_data(gabtag_sources, install_dir: moduledir)
