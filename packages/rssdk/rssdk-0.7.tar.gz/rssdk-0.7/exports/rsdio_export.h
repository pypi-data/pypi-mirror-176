
#ifndef RSDIO_EXPORT_H
#define RSDIO_EXPORT_H

#ifdef RSDIO_STATIC_DEFINE
#  define RSDIO_EXPORT
#  define RSDIO_NO_EXPORT
#else
#  ifndef RSDIO_EXPORT
#    ifdef rsdio_EXPORTS
        /* We are building this library */
#      define RSDIO_EXPORT 
#    else
        /* We are using this library */
#      define RSDIO_EXPORT 
#    endif
#  endif

#  ifndef RSDIO_NO_EXPORT
#    define RSDIO_NO_EXPORT 
#  endif
#endif

#ifndef RSDIO_DEPRECATED
#  define RSDIO_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef RSDIO_DEPRECATED_EXPORT
#  define RSDIO_DEPRECATED_EXPORT RSDIO_EXPORT RSDIO_DEPRECATED
#endif

#ifndef RSDIO_DEPRECATED_NO_EXPORT
#  define RSDIO_DEPRECATED_NO_EXPORT RSDIO_NO_EXPORT RSDIO_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef RSDIO_NO_DEPRECATED
#    define RSDIO_NO_DEPRECATED
#  endif
#endif

#endif /* RSDIO_EXPORT_H */
