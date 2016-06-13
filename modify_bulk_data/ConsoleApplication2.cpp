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
#include <assert.h>  
#include <map>

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


struct RowData
{
    long SeqNo;
    int IndexSampleValue;
    double IndexDisplayValue;
    std::map<string, vector<double>> ChannelValues;
};

struct BulkFileData
{
    wstring fileName;
    std::map<string, ColumnInfoLayout_t> ChannelDataTypes;
    vector<RowData> RowValues;
};

vector<wstring> get_all_htd_files_names_within_folder(wstring folder)
{
    vector<wstring> names;
    wchar_t search_path[200];
    wsprintfW(search_path, L"%s/*.htd", folder.c_str());   // *.htd will filter all *.htd file out.
    WIN32_FIND_DATA fd;
    HANDLE hFind = ::FindFirstFile(search_path, &fd);
    if (hFind != INVALID_HANDLE_VALUE) 
    {
        do 
        {
            // read all (real) files in current folder
            // , delete '!' read other 2 default folder . and ..
            if (!(fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) 
            {
                wstring fullname = folder + L"\\" + fd.cFileName;
                names.push_back(fullname);
            }
        } while (::FindNextFile(hFind, &fd));
        FindClose(hFind);
    }
    return names;
}


wstring get_blb_file_namer(wstring htdFileName)
{

    wstring strReplace = L".blb";
    wstring strDest = L".htd";

    size_t pos = htdFileName.find(strDest);
    wstring blbFileName = htdFileName.replace(pos, strDest.size(), strReplace);

    return blbFileName;
}


BulkFileData LoadData(wstring htd_file)
{

        BulkFileData aBulkFileData;
        aBulkFileData.fileName = htd_file;
        // Open htd file to read header.
        ifstream htd_input_stream(htd_file, std::ios::binary);
        wstring blbFileName = get_blb_file_namer(htd_file);

        ifstream blb_input_stream(blbFileName, std::ios::binary);

        if (!htd_input_stream.is_open())
        {
            std::wcout << L"Fail to open file: " << htd_file << std::endl;
            throw exception();
        }

        if (!blb_input_stream.is_open())
        {
            std::wcout << L"Not found blb file: " << blbFileName << std::endl;
        }
        std::cout << std::endl;
        std::wcout << L"Loading File : " << htd_file << std::endl;

        htd_input_stream.seekg(0, std::ios::beg);

        HeaderLayout_t header = { 0 };

        if (!htd_input_stream.eof())
        {
            htd_input_stream.read((char*)&header, sizeof(HeaderLayout_t));
        }

        aBulkFileData.RowValues.reserve(header.SequenceNumber);
        // Read the column information
        vector<ColumnInfoLayout_t> columns;

        htd_input_stream.seekg(128, std::ios::beg);

        for (unsigned long i = 0; i < header.ColumnCount; i++)
        {
            ColumnInfoLayout_t col = { 0 };
            htd_input_stream.read((char*)&col, sizeof(ColumnInfoLayout_t));
            columns.push_back(col);
            aBulkFileData.ChannelDataTypes[col.m_ColumnName] = col;
        }

        for (size_t seqNo = 0; seqNo < header.SequenceNumber; seqNo++)
        {
            std::cout << "reading row : " << seqNo << "\r";
            RowData rowData;
            if (header.ImplicitIndexDirection == SLB_BULKDATASTORE_INDEX_INCREASING)
            {
                rowData.IndexSampleValue = header.ImplicitIndexStart + header.ImplicitIndexSamplingRate * seqNo;
            }
            else if (header.ImplicitIndexDirection == SLB_BULKDATASTORE_INDEX_DECREASING)
            {
                rowData.IndexSampleValue = header.ImplicitIndexStart - header.ImplicitIndexSamplingRate * seqNo;
            }

            rowData.IndexDisplayValue = (double)rowData.IndexSampleValue / 120.0;
            rowData.SeqNo = seqNo;

            for (auto &column : columns)
            {
                string colname = column.m_ColumnName;

                rowData.ChannelValues[colname] = vector<double>();
 
                if (column.m_ColumnDimensionCount == 1)
                {
                    unsigned long pos = header.HeaderSize + header.RowSize * seqNo + column.m_ColumnOffset;
                    
                    htd_input_stream.seekg(pos, std::ios::beg);
                    
                    BlobBlockHeader block;
                    htd_input_stream.read((char*)&block, sizeof(BlobBlockHeader));
                    //std::cout << "blob Offset: " << std::dec << block.BlobOffset << " Blob Size: " << block.BlobSize << std::endl;
                    
                    if (block.BlobOffset == -1)
                    {
                        continue;
                    }
                    blb_input_stream.seekg(block.BlobOffset, std::ios::beg);
                    long prefacesize;
                    blb_input_stream.read((char*)&prefacesize, sizeof(long));

                    vector<double> oneColValues;
                    oneColValues.reserve(prefacesize);
                    for (long i = 0; i < prefacesize; i++)
                    {
                        double doubleValue;
                        //blb_input_stream.read((char*)&prefacesize, sizeof(long));
                        switch (column.m_ColumnDataType)
                        {
                        case    DATA_TYPE_INT8:
                        case    DATA_TYPE_UINT8:
                        {
                            INT8 value;
                            blb_input_stream.read((char*)&value, sizeof(INT8));
                            oneColValues.push_back(value);
                        }
                        break;
                        case    DATA_TYPE_INT16:
                        case    DATA_TYPE_UINT16:
                        {
                            INT16 value;
                            blb_input_stream.read((char*)&value, sizeof(INT16));

                            oneColValues.push_back(value);
                        }
                        break;
                        case    DATA_TYPE_INT32:
                        case    DATA_TYPE_UINT32:
                        {
                            int value;
                            blb_input_stream.read((char*)&value, sizeof(int));
                            oneColValues.push_back(value);
                        }
                        break;
                        case    DATA_TYPE_IEEE32:
                        {
                            float value;
                            blb_input_stream.read((char*)&value, sizeof(float));
                            oneColValues.push_back(value);

                        }
                        break;

                        case    DATA_TYPE_IEEE64:
                        {
                            double value;
                            blb_input_stream.read((char*)&value, sizeof(double));

                            oneColValues.push_back(value);

                        }
                        break;
                        case    DATA_TYPE_IEEE32_COMPLEX:
                        case    DATA_TYPE_IEEE64_COMPLEX:
                        case    DATA_TYPE_ENUM_LONG:
                        case    DATA_TYPE_ENUM_STRING:
                        case    DATA_TYPE_STRING:
                            throw;
                        default:
                            break;
                        }
                    }
                    rowData.ChannelValues[colname].swap(oneColValues);
                }
                else if (column.m_ColumnDimensionCount == 0)
                {
                    unsigned long pos = header.HeaderSize + header.RowSize * seqNo + column.m_ColumnOffset;
                    htd_input_stream.seekg(pos, std::ios::beg);
                    switch (column.m_ColumnDataType)
                    {
                    case    DATA_TYPE_INT8:
                    case    DATA_TYPE_UINT8:
                    {
                        INT8 value;
                        htd_input_stream.read((char*)&value, sizeof(INT8));
                        rowData.ChannelValues[colname].push_back(value);
                    }
                    break;
                    case    DATA_TYPE_INT16:
                    case    DATA_TYPE_UINT16:
                    {
                        INT16 value;
                        htd_input_stream.read((char*)&value, sizeof(INT16));
                        rowData.ChannelValues[colname].push_back(value);

                    }
                    break;
                    case    DATA_TYPE_INT32:
                    case    DATA_TYPE_UINT32:
                    {
                        int value;
                        htd_input_stream.read((char*)&value, sizeof(int));
                        rowData.ChannelValues[colname].push_back(value);

                    }
                    break;
                    case    DATA_TYPE_IEEE32:
                    {
                        float value;
                        htd_input_stream.read((char*)&value, sizeof(float));
                        rowData.ChannelValues[colname].push_back(value);

                    }
                    break;

                    case    DATA_TYPE_IEEE64:
                    {
                        double value;
                        htd_input_stream.read((char*)&value, sizeof(double));
                        rowData.ChannelValues[colname].push_back(value);

                    }
                        break;
                    case    DATA_TYPE_IEEE32_COMPLEX:
                    case    DATA_TYPE_IEEE64_COMPLEX:
                    case    DATA_TYPE_ENUM_LONG:
                    case    DATA_TYPE_ENUM_STRING:
                    case    DATA_TYPE_STRING:
                        throw ;
                    default:
                        break;
                    }

                }
                else
                    throw;
            }
            aBulkFileData.RowValues.push_back(move(rowData));
         }

       
        htd_input_stream.close();
        blb_input_stream.close();
        std::wcout << L"....DONE...." <<endl;

        return aBulkFileData;
}

int _tmain(int argc, _TCHAR* argv[])
{
    vector<wstring> htd_file_list = get_all_htd_files_names_within_folder(L"D:\\temp\\1");

    for (auto htdFile : htd_file_list)
    {
        BulkFileData data = LoadData(htdFile);
    }

}

