scalable_dir = join_paths('hicolor', 'scalable')

install_data(
  join_paths(scalable_dir, 'apps', ('@0@.svg').format(app_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir, 'apps')
)

install_data(
  join_paths(scalable_dir, 'actions', 'tag-symbolic.svg'),
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir, 'actions')
)

symbolic_dir = join_paths('hicolor', 'symbolic', 'apps')
install_data(
  join_paths(symbolic_dir, 'com.github.lachhebo.Gabtag-symbolic.svg'),
  install_dir: join_paths(get_option('datadir'), 'icons', symbolic_dir),
  rename: '@0@-symbolic.svg'.format(app_id)
)
