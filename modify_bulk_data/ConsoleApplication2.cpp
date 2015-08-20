// ConsoleApplication2.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <intrin.h>
#include <iostream>
#include <tchar.h>
#include <vector>
#include <fstream>
#include <array>
#include <string>
#include <limits>

using namespace std;
using namespace std::tr1;
using std::numeric_limits;


enum DataType
{
	DATA_TYPE_UNKNOWN = 0,
	DATA_TYPE_INT8 = 1,
	DATA_TYPE_UINT8 = 2,
	DATA_TYPE_INT16 = 3,
	DATA_TYPE_UINT16 = 4,
	DATA_TYPE_INT32 = 5,
	DATA_TYPE_UINT32 = 6,
	DATA_TYPE_IEEE32 = 7,
	DATA_TYPE_IEEE64 = 8,
	DATA_TYPE_IEEE32_COMPLEX = 9,
	DATA_TYPE_IEEE64_COMPLEX = 10,
	DATA_TYPE_ENUM_LONG = 11,
	DATA_TYPE_ENUM_STRING = 12,
	DATA_TYPE_STRING = 13
};

enum TableStatus
{
	BDS_TABLESTATUS_CLOSED_FOR_WRITE = 0x0,
	BDS_TABLESTATUS_OPEN_WRITE_NORMAL = 0x1,
	BDS_TABLESTATUS_OPEN_WRITE_RESTRICTED = 0x10,
	BDS_TABLESTATUS_OPEN_WRITE_BOTH = BDS_TABLESTATUS_OPEN_WRITE_NORMAL | BDS_TABLESTATUS_OPEN_WRITE_RESTRICTED,
	// deprecated
	SLB_BULKDATASTORE_TABLESTATUS_OPEN = BDS_TABLESTATUS_OPEN_WRITE_BOTH,
	SLB_BULKDATASTORE_TABLESTATUS_CLOSED = BDS_TABLESTATUS_CLOSED_FOR_WRITE,
	SLB_BULKDATASTORE_TABLESTATUS_OPEN_RESTRICTED = BDS_TABLESTATUS_OPEN_WRITE_RESTRICTED,
	SLB_BULKDATASTORE_TABLESTATUS_OPEN_NORMAL = BDS_TABLESTATUS_OPEN_WRITE_NORMAL
};

enum TableType
{
	BDS_TABLETYPE_NORMAL,
	BDS_TABLETYPE_REFERENCES_BLOB_FILE,
	// deprecated
	SLB_BULKDATASTORE_TABLETYPE_NORMAL = BDS_TABLETYPE_NORMAL,
	SLB_BULKDATASTORE_TABLETYPE_REFERENCES_BLOB_TABLE = BDS_TABLETYPE_REFERENCES_BLOB_FILE
};

enum IndexDirection
{
	BDS_INDEX_DIRECTION_UNKNOWN,
	BDS_INDEX_DIRECTION_INCREASING,
	BDS_INDEX_DIRECTION_DECREASING,
	// deprecated
	SLB_BULKDATASTORE_INDEX_INCREASING = BDS_INDEX_DIRECTION_INCREASING,
	SLB_BULKDATASTORE_INDEX_DECREASING = BDS_INDEX_DIRECTION_DECREASING
};

typedef struct HtdHeaderLayout
{
	unsigned long                   HeaderVersionNo;
	unsigned long                   SequenceNumber;             // row # (0 based) of last row written.
	unsigned long                   RestrictedSequenceNumber;   // Sequence number used by recomputation

	unsigned long                   RowSize;                    // Size of each row in bytes
	unsigned long                   ColumnCount;                // no. of ColumnInfoLayout_t's in header

	TableStatus						tableStatus;                // open/closed
	TableType						tableType;

	unsigned long                   IndexChannel;               // Which column is index channel
	// Only valid for acq doamin, index is Time_1900 which is explicit

	bool                            IndexIsImplicit;            // False means acq domain, true means time or depth domain
	bool                            TimeIndexed;                // Only valid when IndexIsImplicit is true
	// False means depth domain, true means time domain
	bool                            TruncatedFile;              // Flag identifying the file has been properly truncated or not.
	IndexDirection					ImplicitIndexDirection;     // Increasing or descreasing, descreasing is only for depth domain
	double                          ImplicitIndexStart;         // Only valid when IndexIsImplicit is true
	// For time domain, it is start time, for depth domain it is start depth
	double                          ImplicitIndexSamplingRate;  // Only valid when IndexIsImplicit is true
	// For time domain, it is sampling time rate, for depth domain it is sampling depth rate

	double                          IndexStart;                 // Start index value only valid for acq doamin, index is Time_1900 which is explicit
	double                          IndexStop;                  // Stop index value only valid for acq doamin, index is Time_1900 which is explicit

	long                            RemapNumber;                // # of 64k we need to map the whole file
	long                            BlobRemapNumber;            // # of 64k we need to map the whole blob file
	volatile __int64                BlobOffset;                 // Offset to end of blob file (i.e., blob file size), used when re-opening for writing
	long                            RefCount;                   //
	unsigned long                   HeaderSize;                 // Header size including column info layout
	unsigned long                   FlushSequenceNumber;        // SequenceNumber at flush point, used for real time file backup support
	unsigned long                   JumpBackCount;              // Flag to indicate write back happends, used for real time file backup support

} HeaderLayout_t;


typedef struct ColumnInfoLayout
{
    unsigned long   m_ColumnOffset;               // datum's byte offset in data row
    short unsigned  m_ColumnDataType;             // as API DataType
    short unsigned  m_ColumnDimensionCount;       // 0: scalar, 1: vector, 2: matrix, etc.
    char         m_ColumnName[56];
}ColumnInfoLayout_t;




int _tmain(int argc, _TCHAR* argv[])
{
    wstring input_htd_filename =  L"d:\\temp\\1\\empty.htd";

    // Open htd file to read header.
    ifstream is_htd(input_htd_filename, std::ios::binary);
    
    if (!is_htd.is_open())
    {
        std::wcout << L"Fail to open file: " << input_htd_filename << std::endl;
        return -1;
    }

	is_htd.seekg(0, std::ios::beg);

	HeaderLayout_t header = { 0 };
	if (!is_htd.eof())
	{
		is_htd.read((char*)&header, sizeof(HeaderLayout_t));
	}

	unsigned long rowSize = header.RowSize;

    int columnCount = header.ColumnCount;

    is_htd.seekg(128,is_htd.beg);

    vector<ColumnInfoLayout_t> columns;

    // Read column info.  col 0 is RSWMLH, col 1 is SWMLHN
    ColumnInfoLayout_t col = { 0 };
    for (int i = 0; i < columnCount; i++)
    {
        is_htd.read((char*)&col, sizeof(ColumnInfoLayout_t));
        columns.push_back(col);
    }


    is_htd.close();


    header.BlobOffset = 0;
    header.TruncatedFile = FALSE;
    header.SequenceNumber = -1;
    header.RestrictedSequenceNumber = -1;
    header.IndexStart = std::numeric_limits<double>::quiet_NaN();
    header.IndexStop = std::numeric_limits<double>::quiet_NaN();


    fstream os_htd(input_htd_filename, std::ios::binary  | ios::in | ios::out);
    
    streampos end;
    os_htd.seekg(0, ios::end);
    end = os_htd.tellg();

    os_htd.seekp(0, ios_base::beg);
    os_htd.write((char*)&header, sizeof(HeaderLayout_t));

    os_htd.seekp(header.HeaderSize, ios_base::beg);

    while (os_htd.tellp() != end)
    {
        os_htd.put('\0');
    }

    os_htd.close();


	return 0;
}

