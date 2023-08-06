
#include <Python.h>
#include <stddef.h>

/* this block of #ifs should be kept exactly identical between
   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py
   and cffi/_cffi_include.h */
#if defined(_MSC_VER)
# include <malloc.h>   /* for alloca() */
# if _MSC_VER < 1600   /* MSVC < 2010 */
   typedef __int8 int8_t;
   typedef __int16 int16_t;
   typedef __int32 int32_t;
   typedef __int64 int64_t;
   typedef unsigned __int8 uint8_t;
   typedef unsigned __int16 uint16_t;
   typedef unsigned __int32 uint32_t;
   typedef unsigned __int64 uint64_t;
   typedef __int8 int_least8_t;
   typedef __int16 int_least16_t;
   typedef __int32 int_least32_t;
   typedef __int64 int_least64_t;
   typedef unsigned __int8 uint_least8_t;
   typedef unsigned __int16 uint_least16_t;
   typedef unsigned __int32 uint_least32_t;
   typedef unsigned __int64 uint_least64_t;
   typedef __int8 int_fast8_t;
   typedef __int16 int_fast16_t;
   typedef __int32 int_fast32_t;
   typedef __int64 int_fast64_t;
   typedef unsigned __int8 uint_fast8_t;
   typedef unsigned __int16 uint_fast16_t;
   typedef unsigned __int32 uint_fast32_t;
   typedef unsigned __int64 uint_fast64_t;
   typedef __int64 intmax_t;
   typedef unsigned __int64 uintmax_t;
# else
#  include <stdint.h>
# endif
# if _MSC_VER < 1800   /* MSVC < 2013 */
#  ifndef __cplusplus
    typedef unsigned char _Bool;
#  endif
# endif
#else
# include <stdint.h>
# if (defined (__SVR4) && defined (__sun)) || defined(_AIX) || defined(__hpux)
#  include <alloca.h>
# endif
#endif

#if PY_MAJOR_VERSION < 3
# undef PyCapsule_CheckExact
# undef PyCapsule_GetPointer
# define PyCapsule_CheckExact(capsule) (PyCObject_Check(capsule))
# define PyCapsule_GetPointer(capsule, name) \
    (PyCObject_AsVoidPtr(capsule))
#endif

#if PY_MAJOR_VERSION >= 3
# define PyInt_FromLong PyLong_FromLong
#endif

#define _cffi_from_c_double PyFloat_FromDouble
#define _cffi_from_c_float PyFloat_FromDouble
#define _cffi_from_c_long PyInt_FromLong
#define _cffi_from_c_ulong PyLong_FromUnsignedLong
#define _cffi_from_c_longlong PyLong_FromLongLong
#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong
#define _cffi_from_c__Bool PyBool_FromLong

#define _cffi_to_c_double PyFloat_AsDouble
#define _cffi_to_c_float PyFloat_AsDouble

#define _cffi_from_c_int_const(x)                                        \
    (((x) > 0) ?                                                         \
        ((unsigned long long)(x) <= (unsigned long long)LONG_MAX) ?      \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromUnsignedLongLong((unsigned long long)(x)) :       \
        ((long long)(x) >= (long long)LONG_MIN) ?                        \
            PyInt_FromLong((long)(x)) :                                  \
            PyLong_FromLongLong((long long)(x)))

#define _cffi_from_c_int(x, type)                                        \
    (((type)-1) > 0 ? /* unsigned */                                     \
        (sizeof(type) < sizeof(long) ?                                   \
            PyInt_FromLong((long)x) :                                    \
         sizeof(type) == sizeof(long) ?                                  \
            PyLong_FromUnsignedLong((unsigned long)x) :                  \
            PyLong_FromUnsignedLongLong((unsigned long long)x)) :        \
        (sizeof(type) <= sizeof(long) ?                                  \
            PyInt_FromLong((long)x) :                                    \
            PyLong_FromLongLong((long long)x)))

#define _cffi_to_c_int(o, type)                                          \
    ((type)(                                                             \
     sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \
                                         : (type)_cffi_to_c_i8(o)) :     \
     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \
                                         : (type)_cffi_to_c_i16(o)) :    \
     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \
                                         : (type)_cffi_to_c_i32(o)) :    \
     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \
                                         : (type)_cffi_to_c_i64(o)) :    \
     (Py_FatalError("unsupported size for type " #type), (type)0)))

#define _cffi_to_c_i8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[1])
#define _cffi_to_c_u8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[2])
#define _cffi_to_c_i16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[3])
#define _cffi_to_c_u16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[4])
#define _cffi_to_c_i32                                                   \
                 ((int(*)(PyObject *))_cffi_exports[5])
#define _cffi_to_c_u32                                                   \
                 ((unsigned int(*)(PyObject *))_cffi_exports[6])
#define _cffi_to_c_i64                                                   \
                 ((long long(*)(PyObject *))_cffi_exports[7])
#define _cffi_to_c_u64                                                   \
                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])
#define _cffi_to_c_char                                                  \
                 ((int(*)(PyObject *))_cffi_exports[9])
#define _cffi_from_c_pointer                                             \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[10])
#define _cffi_to_c_pointer                                               \
    ((char *(*)(PyObject *, CTypeDescrObject *))_cffi_exports[11])
#define _cffi_get_struct_layout                                          \
    ((PyObject *(*)(Py_ssize_t[]))_cffi_exports[12])
#define _cffi_restore_errno                                              \
    ((void(*)(void))_cffi_exports[13])
#define _cffi_save_errno                                                 \
    ((void(*)(void))_cffi_exports[14])
#define _cffi_from_c_char                                                \
    ((PyObject *(*)(char))_cffi_exports[15])
#define _cffi_from_c_deref                                               \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[16])
#define _cffi_to_c                                                       \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[17])
#define _cffi_from_c_struct                                              \
    ((PyObject *(*)(char *, CTypeDescrObject *))_cffi_exports[18])
#define _cffi_to_c_wchar_t                                               \
    ((wchar_t(*)(PyObject *))_cffi_exports[19])
#define _cffi_from_c_wchar_t                                             \
    ((PyObject *(*)(wchar_t))_cffi_exports[20])
#define _cffi_to_c_long_double                                           \
    ((long double(*)(PyObject *))_cffi_exports[21])
#define _cffi_to_c__Bool                                                 \
    ((_Bool(*)(PyObject *))_cffi_exports[22])
#define _cffi_prepare_pointer_call_argument                              \
    ((Py_ssize_t(*)(CTypeDescrObject *, PyObject *, char **))_cffi_exports[23])
#define _cffi_convert_array_from_object                                  \
    ((int(*)(char *, CTypeDescrObject *, PyObject *))_cffi_exports[24])
#define _CFFI_NUM_EXPORTS 25

typedef struct _ctypedescr CTypeDescrObject;

static void *_cffi_exports[_CFFI_NUM_EXPORTS];
static PyObject *_cffi_types, *_cffi_VerificationError;

static int _cffi_setup_custom(PyObject *lib);   /* forward */

static PyObject *_cffi_setup(PyObject *self, PyObject *args)
{
    PyObject *library;
    int was_alive = (_cffi_types != NULL);
    (void)self; /* unused */
    if (!PyArg_ParseTuple(args, "OOO", &_cffi_types, &_cffi_VerificationError,
                                       &library))
        return NULL;
    Py_INCREF(_cffi_types);
    Py_INCREF(_cffi_VerificationError);
    if (_cffi_setup_custom(library) < 0)
        return NULL;
    return PyBool_FromLong(was_alive);
}

union _cffi_union_alignment_u {
    unsigned char m_char;
    unsigned short m_short;
    unsigned int m_int;
    unsigned long m_long;
    unsigned long long m_longlong;
    float m_float;
    double m_double;
    long double m_longdouble;
};

struct _cffi_freeme_s {
    struct _cffi_freeme_s *next;
    union _cffi_union_alignment_u alignment;
};

#ifdef __GNUC__
  __attribute__((unused))
#endif
static int _cffi_convert_array_argument(CTypeDescrObject *ctptr, PyObject *arg,
                                        char **output_data, Py_ssize_t datasize,
                                        struct _cffi_freeme_s **freeme)
{
    char *p;
    if (datasize < 0)
        return -1;

    p = *output_data;
    if (p == NULL) {
        struct _cffi_freeme_s *fp = (struct _cffi_freeme_s *)PyObject_Malloc(
            offsetof(struct _cffi_freeme_s, alignment) + (size_t)datasize);
        if (fp == NULL)
            return -1;
        fp->next = *freeme;
        *freeme = fp;
        p = *output_data = (char *)&fp->alignment;
    }
    memset((void *)p, 0, (size_t)datasize);
    return _cffi_convert_array_from_object(p, ctptr, arg);
}

#ifdef __GNUC__
  __attribute__((unused))
#endif
static void _cffi_free_array_arguments(struct _cffi_freeme_s *freeme)
{
    do {
        void *p = (void *)freeme;
        freeme = freeme->next;
        PyObject_Free(p);
    } while (freeme != NULL);
}

static int _cffi_init(void)
{
    PyObject *module, *c_api_object = NULL;

    module = PyImport_ImportModule("_cffi_backend");
    if (module == NULL)
        goto failure;

    c_api_object = PyObject_GetAttrString(module, "_C_API");
    if (c_api_object == NULL)
        goto failure;
    if (!PyCapsule_CheckExact(c_api_object)) {
        PyErr_SetNone(PyExc_ImportError);
        goto failure;
    }
    memcpy(_cffi_exports, PyCapsule_GetPointer(c_api_object, "cffi"),
           _CFFI_NUM_EXPORTS * sizeof(void *));

    Py_DECREF(module);
    Py_DECREF(c_api_object);
    return 0;

  failure:
    Py_XDECREF(module);
    Py_XDECREF(c_api_object);
    return -1;
}

#define _cffi_type(num) ((CTypeDescrObject *)PyList_GET_ITEM(_cffi_types, num))

/**********/



#include <sys/types.h>
#include <libnfnetlink/libnfnetlink.h>
#include <libnetfilter_log/libnetfilter_log.h>
#include <libnetfilter_log/linux_nfnetlink_log.h>


static int _cffi_const_NFULNL_COPY_PACKET(PyObject *lib)
{
  PyObject *o;
  int res;
  o = _cffi_from_c_int_const(NFULNL_COPY_PACKET);
  if (o == NULL)
    return -1;
  res = PyObject_SetAttrString(lib, "NFULNL_COPY_PACKET", o);
  Py_DECREF(o);
  if (res < 0)
    return -1;
  return ((void)lib,0);
}

static PyObject *
_cffi_f_nflog_bind_group(PyObject *self, PyObject *args)
{
  struct nflog_handle * x0;
  unsigned short x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  struct nflog_g_handle * result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_bind_group", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(0), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned short);
  if (x1 == (unsigned short)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_bind_group(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_pointer((char *)result, _cffi_type(1));
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_bind_pf(PyObject *self, PyObject *args)
{
  struct nflog_handle * x0;
  unsigned short x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_bind_pf", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(0), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned short);
  if (x1 == (unsigned short)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_bind_pf(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_callback_register(PyObject *self, PyObject *args)
{
  struct nflog_g_handle * x0;
  int(* x1)(struct nflog_g_handle *, struct nfgenmsg *, struct nflog_data *, void *);
  void * x2;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:nflog_callback_register", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(1), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x1 = (int(*)(struct nflog_g_handle *, struct nfgenmsg *, struct nflog_data *, void *))_cffi_to_c_pointer(arg1, _cffi_type(2));
  if (x1 == (int(*)(struct nflog_g_handle *, struct nfgenmsg *, struct nflog_data *, void *))NULL && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg2, (char **)&x2);
  if (datasize != 0) {
    x2 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(3), arg2, (char **)&x2,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_callback_register(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_fd(PyObject *self, PyObject *arg0)
{
  struct nflog_handle * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(0), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_fd(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_gid(PyObject *self, PyObject *args)
{
  struct nflog_data * x0;
  unsigned int * x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_get_gid", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    x1 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(5), arg1, (char **)&x1,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_gid(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_hwtype(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  unsigned short result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_hwtype(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, unsigned short);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_indev(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  unsigned int result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_indev(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, unsigned int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_msg_packet_hdr(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  struct nfulnl_msg_packet_hdr * result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_msg_packet_hdr(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_pointer((char *)result, _cffi_type(6));
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_msg_packet_hwhdr(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  char * result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_msg_packet_hwhdr(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_pointer((char *)result, _cffi_type(7));
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_msg_packet_hwhdrlen(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  unsigned short result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_msg_packet_hwhdrlen(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, unsigned short);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_nfmark(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  unsigned int result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_nfmark(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, unsigned int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_outdev(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  unsigned int result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_outdev(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, unsigned int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_packet_hw(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  struct nfulnl_msg_packet_hw * result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_packet_hw(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_pointer((char *)result, _cffi_type(8));
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_payload(PyObject *self, PyObject *args)
{
  struct nflog_data * x0;
  char * * x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_get_payload", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(9), arg1, (char **)&x1);
  if (datasize != 0) {
    x1 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(9), arg1, (char **)&x1,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_payload(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_physindev(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  unsigned int result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_physindev(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, unsigned int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_physoutdev(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  unsigned int result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_physoutdev(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, unsigned int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_prefix(PyObject *self, PyObject *arg0)
{
  struct nflog_data * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  char * result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_prefix(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_pointer((char *)result, _cffi_type(7));
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_seq(PyObject *self, PyObject *args)
{
  struct nflog_data * x0;
  unsigned int * x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_get_seq", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    x1 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(5), arg1, (char **)&x1,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_seq(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_seq_global(PyObject *self, PyObject *args)
{
  struct nflog_data * x0;
  unsigned int * x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_get_seq_global", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    x1 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(5), arg1, (char **)&x1,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_seq_global(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_timestamp(PyObject *self, PyObject *args)
{
  struct nflog_data * x0;
  struct timeval * x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_get_timestamp", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(10), arg1, (char **)&x1);
  if (datasize != 0) {
    x1 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(10), arg1, (char **)&x1,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_timestamp(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_get_uid(PyObject *self, PyObject *args)
{
  struct nflog_data * x0;
  unsigned int * x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_get_uid", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(4), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(4), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(5), arg1, (char **)&x1);
  if (datasize != 0) {
    x1 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(5), arg1, (char **)&x1,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_get_uid(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_handle_packet(PyObject *self, PyObject *args)
{
  struct nflog_handle * x0;
  char * x1;
  int x2;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:nflog_handle_packet", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(0), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(7), arg1, (char **)&x1);
  if (datasize != 0) {
    x1 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(7), arg1, (char **)&x1,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, int);
  if (x2 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_handle_packet(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_open(PyObject *self, PyObject *noarg)
{
  struct nflog_handle * result;
  PyObject *pyresult;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_open(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  pyresult = _cffi_from_c_pointer((char *)result, _cffi_type(0));
  return pyresult;
}

static PyObject *
_cffi_f_nflog_set_flags(PyObject *self, PyObject *args)
{
  struct nflog_g_handle * x0;
  unsigned short x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_set_flags", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(1), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned short);
  if (x1 == (unsigned short)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_set_flags(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_set_mode(PyObject *self, PyObject *args)
{
  struct nflog_g_handle * x0;
  unsigned char x1;
  unsigned int x2;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;

  if (!PyArg_ParseTuple(args, "OOO:nflog_set_mode", &arg0, &arg1, &arg2))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(1), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned char);
  if (x1 == (unsigned char)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, unsigned int);
  if (x2 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_set_mode(x0, x1, x2); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_set_nlbufsiz(PyObject *self, PyObject *args)
{
  struct nflog_g_handle * x0;
  unsigned int x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_set_nlbufsiz", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(1), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned int);
  if (x1 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_set_nlbufsiz(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_set_qthresh(PyObject *self, PyObject *args)
{
  struct nflog_g_handle * x0;
  unsigned int x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_set_qthresh", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(1), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned int);
  if (x1 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_set_qthresh(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_set_timeout(PyObject *self, PyObject *args)
{
  struct nflog_g_handle * x0;
  unsigned int x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_set_timeout", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(1), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned int);
  if (x1 == (unsigned int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_set_timeout(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_unbind_group(PyObject *self, PyObject *arg0)
{
  struct nflog_g_handle * x0;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(1), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(1), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_unbind_group(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_nflog_unbind_pf(PyObject *self, PyObject *args)
{
  struct nflog_handle * x0;
  unsigned short x1;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  int result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_ParseTuple(args, "OO:nflog_unbind_pf", &arg0, &arg1))
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(0), arg0, (char **)&x0);
  if (datasize != 0) {
    x0 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(0), arg0, (char **)&x0,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x1 = _cffi_to_c_int(arg1, unsigned short);
  if (x1 == (unsigned short)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = nflog_unbind_pf(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, int);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static PyObject *
_cffi_f_recv(PyObject *self, PyObject *args)
{
  int x0;
  void * x1;
  size_t x2;
  int x3;
  Py_ssize_t datasize;
  struct _cffi_freeme_s *large_args_free = NULL;
  ssize_t result;
  PyObject *pyresult;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;

  if (!PyArg_ParseTuple(args, "OOOO:recv", &arg0, &arg1, &arg2, &arg3))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(3), arg1, (char **)&x1);
  if (datasize != 0) {
    x1 = ((size_t)datasize) <= 640 ? alloca((size_t)datasize) : NULL;
    if (_cffi_convert_array_argument(_cffi_type(3), arg1, (char **)&x1,
            datasize, &large_args_free) < 0)
      return NULL;
  }

  x2 = _cffi_to_c_int(arg2, size_t);
  if (x2 == (size_t)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, int);
  if (x3 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = recv(x0, x1, x2, x3); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  pyresult = _cffi_from_c_int(result, ssize_t);
  if (large_args_free != NULL) _cffi_free_array_arguments(large_args_free);
  return pyresult;
}

static void _cffi_check_struct_timeval(struct timeval *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->tv_sec) << 1);
  (void)((p->tv_usec) << 1);
}
static PyObject *
_cffi_layout_struct_timeval(PyObject *self, PyObject *noarg)
{
  struct _cffi_aligncheck { char x; struct timeval y; };
  static Py_ssize_t nums[] = {
    sizeof(struct timeval),
    offsetof(struct _cffi_aligncheck, y),
    offsetof(struct timeval, tv_sec),
    sizeof(((struct timeval *)0)->tv_sec),
    offsetof(struct timeval, tv_usec),
    sizeof(((struct timeval *)0)->tv_usec),
    -1
  };
  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_get_struct_layout(nums);
  /* the next line is not executed, but compiled */
  _cffi_check_struct_timeval(0);
}

static int _cffi_setup_custom(PyObject *lib)
{
  return _cffi_const_NFULNL_COPY_PACKET(lib);
}

static PyMethodDef _cffi_methods[] = {
  {"nflog_bind_group", _cffi_f_nflog_bind_group, METH_VARARGS, NULL},
  {"nflog_bind_pf", _cffi_f_nflog_bind_pf, METH_VARARGS, NULL},
  {"nflog_callback_register", _cffi_f_nflog_callback_register, METH_VARARGS, NULL},
  {"nflog_fd", _cffi_f_nflog_fd, METH_O, NULL},
  {"nflog_get_gid", _cffi_f_nflog_get_gid, METH_VARARGS, NULL},
  {"nflog_get_hwtype", _cffi_f_nflog_get_hwtype, METH_O, NULL},
  {"nflog_get_indev", _cffi_f_nflog_get_indev, METH_O, NULL},
  {"nflog_get_msg_packet_hdr", _cffi_f_nflog_get_msg_packet_hdr, METH_O, NULL},
  {"nflog_get_msg_packet_hwhdr", _cffi_f_nflog_get_msg_packet_hwhdr, METH_O, NULL},
  {"nflog_get_msg_packet_hwhdrlen", _cffi_f_nflog_get_msg_packet_hwhdrlen, METH_O, NULL},
  {"nflog_get_nfmark", _cffi_f_nflog_get_nfmark, METH_O, NULL},
  {"nflog_get_outdev", _cffi_f_nflog_get_outdev, METH_O, NULL},
  {"nflog_get_packet_hw", _cffi_f_nflog_get_packet_hw, METH_O, NULL},
  {"nflog_get_payload", _cffi_f_nflog_get_payload, METH_VARARGS, NULL},
  {"nflog_get_physindev", _cffi_f_nflog_get_physindev, METH_O, NULL},
  {"nflog_get_physoutdev", _cffi_f_nflog_get_physoutdev, METH_O, NULL},
  {"nflog_get_prefix", _cffi_f_nflog_get_prefix, METH_O, NULL},
  {"nflog_get_seq", _cffi_f_nflog_get_seq, METH_VARARGS, NULL},
  {"nflog_get_seq_global", _cffi_f_nflog_get_seq_global, METH_VARARGS, NULL},
  {"nflog_get_timestamp", _cffi_f_nflog_get_timestamp, METH_VARARGS, NULL},
  {"nflog_get_uid", _cffi_f_nflog_get_uid, METH_VARARGS, NULL},
  {"nflog_handle_packet", _cffi_f_nflog_handle_packet, METH_VARARGS, NULL},
  {"nflog_open", _cffi_f_nflog_open, METH_NOARGS, NULL},
  {"nflog_set_flags", _cffi_f_nflog_set_flags, METH_VARARGS, NULL},
  {"nflog_set_mode", _cffi_f_nflog_set_mode, METH_VARARGS, NULL},
  {"nflog_set_nlbufsiz", _cffi_f_nflog_set_nlbufsiz, METH_VARARGS, NULL},
  {"nflog_set_qthresh", _cffi_f_nflog_set_qthresh, METH_VARARGS, NULL},
  {"nflog_set_timeout", _cffi_f_nflog_set_timeout, METH_VARARGS, NULL},
  {"nflog_unbind_group", _cffi_f_nflog_unbind_group, METH_O, NULL},
  {"nflog_unbind_pf", _cffi_f_nflog_unbind_pf, METH_VARARGS, NULL},
  {"recv", _cffi_f_recv, METH_VARARGS, NULL},
  {"_cffi_layout_struct_timeval", _cffi_layout_struct_timeval, METH_NOARGS, NULL},
  {"_cffi_setup", _cffi_setup, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}    /* Sentinel */
};

#if PY_MAJOR_VERSION >= 3

static struct PyModuleDef _cffi_module_def = {
  PyModuleDef_HEAD_INIT,
  "_cffi__x11d28b3fx52abb3c3",
  NULL,
  -1,
  _cffi_methods,
  NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC
PyInit__cffi__x11d28b3fx52abb3c3(void)
{
  PyObject *lib;
  lib = PyModule_Create(&_cffi_module_def);
  if (lib == NULL)
    return NULL;
  if (((void)lib,0) < 0 || _cffi_init() < 0) {
    Py_DECREF(lib);
    return NULL;
  }
  return lib;
}

#else

PyMODINIT_FUNC
init_cffi__x11d28b3fx52abb3c3(void)
{
  PyObject *lib;
  lib = Py_InitModule("_cffi__x11d28b3fx52abb3c3", _cffi_methods);
  if (lib == NULL)
    return;
  if (((void)lib,0) < 0 || _cffi_init() < 0)
    return;
  return;
}

#endif
