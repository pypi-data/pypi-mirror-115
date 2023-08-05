/**
 *  Copyright (c) 2015 by Contributors
 * @file   unistd.h
 * @brief  This file intended to serve as a drop-in replacement for
 * unistd.h on Windows Please add functionality as neeeded
 */
#ifndef PS_WINDOWS_UNISTD_H_
#define PS_WINDOWS_UNISTD_H_
#include <stdlib.h>
#include <io.h>
// #include "getopt.h" /* getopt at: https://gist.github.com/ashelly/7776712 */
#include <process.h> /* for getpid() and the exec..() family */
#include <direct.h> /* for _getcwd() and _chdir() */

#define srandom srand
#define random rand

/* Values for the second argument to access.
   These may be OR'd together.  */
#define R_OK    4       /* Test for read permission.  */
#define W_OK    2       /* Test for write permission.  */
// #define   X_OK    1       /* execute permission - unsupported in windows*/
#define F_OK    0       /* Test for existence.  */

#define access _access
#define dup2 _dup2
#define execve _execve
#define ftruncate _chsize
#define unlink _unlink
#define fileno _fileno
#define getcwd _getcwd
#define chdir _chdir
#define isatty _isatty
#define lseek _lseek

// read, write, and close are NOT being #defined here, because while there are
// file handle specific versions for Windows, they probably don't work for
// sockets. You need to look at your app and consider whether to call
// e.g. closesocket().

#define ssize_t int

#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
/* should be in some equivalent to <sys/types.h> */

#endif  // PS_WINDOWS_UNISTD_H_
