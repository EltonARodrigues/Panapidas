project('panapidas',
          version: '1.0.0',
    meson_version: '>= 1.0.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

application_id = 'dev.eltonarodrigues.panapidas'
project_name = 'Panapidas'

if get_option('profile') == 'development'
  profile = 'Devel'
  application_id = '@0@.Devel'.format(application_id)
  version = ''.join(
    [
      run_command('git', 'describe', '--long', '--tags', check: false).stdout().strip(),
    ],
  )
else
  profile = ''
  version = meson.project_version()
endif

i18n = import('i18n')
python = import('python')
gnome = import('gnome')

python_bin = python.find_installation(
  'python3',
  modules: [],
)


python_dir = python_bin.get_install_dir()


subdir('data')
subdir('panapidas')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
