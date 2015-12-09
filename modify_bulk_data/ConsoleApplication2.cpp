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


struct BlobBlockHeader
{
    __int64 BlobOffset;                        //data type change from unsigned long to __int64 to support over 4G file
    unsigned long BlobSize;
};



int _tmain(int argc, _TCHAR* argv[])
{
    wstring input_htd_filename =  L"d:\\Temp\\1\\0_2_HRGD_LQC_STAT_9E3FFF01-C056-4C85-8773-12CAF9737730_.htd";

    // Open htd file to read header.
    ifstream htd_input_stream(input_htd_filename, std::ios::binary);
    
    if (!htd_input_stream.is_open())
    {
        std::wcout << L"Fail to open file: " << input_htd_filename << std::endl;
        return -1;
    }

	htd_input_stream.seekg(0, std::ios::beg);

	HeaderLayout_t header = { 0 };
    
	if (!htd_input_stream.eof())
	{
		htd_input_stream.read((char*)&header, sizeof(HeaderLayout_t));
	}

    // Read the column information
    vector<ColumnInfoLayout_t> columns;
    DWORD dwRead;

    htd_input_stream.seekg(128, std::ios::beg);

    for (unsigned long seqNo = 0; seqNo < header.ColumnCount; seqNo++)
    {
        ColumnInfoLayout_t col = { 0 };
        htd_input_stream.read((char*)&col, sizeof(ColumnInfoLayout_t));
        columns.push_back(col);
    }


    htd_input_stream.seekg(header.HeaderSize, std::ios::beg);


        for (auto itor = columns.begin(); itor != columns.end(); itor++)
        {
            std::cout << itor->m_ColumnName << ": " << std::endl;
            for (size_t seqNo = 0; seqNo < header.SequenceNumber; seqNo++)
            {
                if (itor->m_ColumnDimensionCount > 0)
                {
                    LARGE_INTEGER liDistanceToMove;
                    unsigned long pos = header.HeaderSize + header.RowSize * seqNo + itor->m_ColumnOffset;
                
                    htd_input_stream.seekg(pos, std::ios::beg );

                    BlobBlockHeader blobHeader;

                    //::ReadFile(hFile, &blobHeader, sizeof(BlobBlockHeader), &dwRead, 0);

                    BlobBlockHeader block;
                    htd_input_stream.read((char*)&block, sizeof(BlobBlockHeader));
                    std::cout << "blob Offset: " << std::dec << block.BlobOffset << " Blob Size: " << block.BlobSize << std::endl;
                }
            }
        }

    htd_input_stream.close();

	return 0;
}

