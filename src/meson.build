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
  'gi_composites.py',
  'main.py',
  'model.py',
  'view.py',
  'window.py',
  'moteur.py',
  'audiobasics.py',
  'MP3Handler.py',
  'data_crawler.py',
  'Crawler_dir.py',
  'Crawler_modif.py',
  'treeview.py'
]

install_data(gabtag_sources, install_dir: moduledir)
