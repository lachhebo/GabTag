pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'gabtag')
gnome = import('gnome')

gnome.compile_resources('gabtag',
  'gabtag.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'gabtag.in',
  output: 'gabtag',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

gabtag_sources = [
  '__init__.py',
  'main.py',
  'version.py',

  'exception.py',
  'tools.py',
  'model.py',

  'treeview.py',
  'view.py',
  'window.py',

  'audio_extension_handler.py',
  'audio_getter.py',
  'audio_mp3_file_handler.py',

  'crawler_data.py',
  'crawler_directory.py',
  'crawler_modification.py',

  'logger.py'
]

install_data(gabtag_sources, install_dir: moduledir)
