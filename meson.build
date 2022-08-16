project('gabtag',
        version: '8',
  meson_version: '>= 0.59.0',
default_options: [ 'warning_level=2',
                 ],
)

i18n = import('i18n')
gnome = import('gnome')

if get_option('devel')
  app_id = 'com.github.lachhebo.Gabtag.Devel'
else
  app_id = 'com.github.lachhebo.Gabtag'
endif

subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
