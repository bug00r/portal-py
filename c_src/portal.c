#include "Python.h"
#include <stdio.h>
#include <wchar.h>

static wchar_t ** convert_args(int argc, char **argv) {
	wchar_t **result = malloc(argc * sizeof(wchar_t *));
	for (int i = 0; i < argc; ++i) {
		size_t len = strlen(argv[i]);
		//result[i] = _Py_char2wchar(argv[i], &len);
        #if PY_VER == 34
        result[i] = _Py_char2wchar(argv[i], &len);
        #else
        result[i] = Py_DecodeLocale(argv[i], &len);
        #endif
	}
	return result;
}

int 
main(int argc, char **argv)
{
	size_t len = strlen(argv[0]);
	#if PY_VER == 34
	wchar_t *program = _Py_char2wchar(argv[0], &len);
    #else
    wchar_t *program = Py_DecodeLocale(argv[0], &len);
    #endif
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }
	#if 0
	//This is need to execute tools absolute => pypath
	#endif
    Py_SetProgramName(program);
	Py_Initialize();
	wchar_t ** wargs = convert_args(argc, argv);
	PySys_SetArgvEx(argc, wargs, 0);
	PyRun_SimpleString("import sys; sys.path.append(\"lib\"); sys.path.append(\"lib/portal_src\"); sys.path.append(\"lib/portal_src/ext\"); import start; start.main()\n");
	
	if(Py_IsInitialized()) {
		Py_Finalize();
	} else {
		printf("W: Python was not initialized!!!");
	}

	return EXIT_SUCCESS;
}
