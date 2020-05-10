#ifndef __GTABLE_H
#define __GTABLE_H
/***********************************************
*  Header for Graphical tables
*  Command line interface for modifying tables
************************************************/

#include "table.h"
#include "basicTypes.h"
#include "vector.h"
#include <stdarg.h>
#include <stdbool.h>

typedef struct {
   Table * table;
   String ** formatCol;
   int * colTypes;
   bool isFixedSize; // fixed row size?
} GTable;

// ... = basic types
GTable * gtable_new(FreeFunc freeFunc, int rows, int cols, ...);

void gtable_destroy(GTable * table);

// ... = default values for row
void gtable_setDefaults(GTable * table, ...);

// ... = list of strings
void gtable_addHeader(GTable * table, ...);
// ... = row data
void gtable_addRow(GTable * table, ...);
//  ... = pointers where to store data
void gtable_getRow(GTable * table, int row, ...);

void gtable_setColWidth(GTable * table, int col, int width);
void gtable_autoSizeColumns(GTable * table);

bool gtable_processInput(GTable * table, String * input);

void * gtable_get(GTable * table, int row, int column);
// Set <column> [<row range>] to <val> [incrementing [by <x>]] [advancing by <y>]
bool gtable_set(GTable * table, Vector * input);
// Swap Rows <row range> and <row range>
bool gtable_swapRows(GTable * table, Vector * v);
// Replace row(s) <row range> with row(s) <row range> [columns <col range>]
bool gtable_replaceRows(GTable * table, Vector * v);
// Add [<n>] row(s) [matching row(s) <row range>]
bool gtable_addRows(GTable * table, Vector * v);
// Delete Row(s) [<row range>]
bool gtable_deleteRows(GTable * table, Vector * v);
// Insert [<n>] Row(s) at <i> [matching row(s) <row range>]
bool gtable_insertRows(GTable * table, Vector * v);

bool gtable_setValue(GTable * table, int row, int col, String * value);
bool gtable_setIntValue(GTable * table, int row, int col, double value);
bool gtable_validRow(GTable * table, String * row, int * start, int * finish);
bool gtable_validCol(GTable * table, String * col, int * start, int * finish);

void gtable_print(GTable * table);

#endif
