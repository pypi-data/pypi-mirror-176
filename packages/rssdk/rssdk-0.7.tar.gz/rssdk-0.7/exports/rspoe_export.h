
#ifndef RSPOE_EXPORT_H
#define RSPOE_EXPORT_H

#ifdef RSPOE_STATIC_DEFINE
#  define RSPOE_EXPORT
#  define RSPOE_NO_EXPORT
#else
#  ifndef RSPOE_EXPORT
#    ifdef rspoe_EXPORTS
        /* We are building this library */
#      define RSPOE_EXPORT 
#    else
        /* We are using this library */
#      define RSPOE_EXPORT 
#    endif
#  endif

#  ifndef RSPOE_NO_EXPORT
#    define RSPOE_NO_EXPORT 
#  endif
#endif

#ifndef RSPOE_DEPRECATED
#  define RSPOE_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef RSPOE_DEPRECATED_EXPORT
#  define RSPOE_DEPRECATED_EXPORT RSPOE_EXPORT RSPOE_DEPRECATED
#endif

#ifndef RSPOE_DEPRECATED_NO_EXPORT
#  define RSPOE_DEPRECATED_NO_EXPORT RSPOE_NO_EXPORT RSPOE_DEPRECATED
#endif

#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef RSPOE_NO_DEPRECATED
#    define RSPOE_NO_DEPRECATED
#  endif
#endif

#endif /* RSPOE_EXPORT_H */
