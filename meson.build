project('gabtag',
        version: '1.5.0',
        meson_version: '>= 0.50.1',
)

i18n = import('i18n')


subdir('data')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')
