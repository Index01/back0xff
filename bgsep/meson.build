bgsep_sources = [
  'gstback0xffbgsep.c',
]

bgsep_deps = dependency('opencv')

if bgsep_deps.found()
  bgsep = library('bgsep',
    bgsep_sources,
    c_args : gst_plugins_bad_args,
    link_args : noseh_link_args,
    include_directories : [libsinc, configinc],
    dependencies : [gstbase_dep, bgsep_deps, gstvideo_dep],
    install : true,
    install_dir : plugins_install_dir,
  )
  pkgconfig.generate(bgsep, install_dir : plugins_pkgconfig_install_dir)
endif
