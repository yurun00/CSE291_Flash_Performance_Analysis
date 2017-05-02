#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <cstdlib>
using namespace std;

int main(int argc, char *argv[]) {
  //argv[1] for input file, argv[2] for size;
  //argv[3] for bw output, argv[4] for iops output, argv[5] for lat output;
  if (argc < 6) {
    cout << "option error: " << endl;
    cout << "argv[1] for input file, argv[2] for size, "
    "argv[3] for bw output, argv[4] for iops output, argv[5] for lat output" << endl;
    return 0;
  }
  const int size = atoi(argv[2]);
  ifstream iFile;
  iFile.open(argv[1]);
  if (!iFile) {
    cout << "File open error!" << endl;
    return 0;
  }
  string line;
  float bw[size];
  float iops[size];
  float lat[size];
  int index = 0;
  while (getline(iFile, line)) {
    getline(iFile, line);
    if (!iFile) {
      cout << "end" << endl;
      break;
    }
    string junk;
    istringstream istream;
    istream.str(line);
    for (int i = 0; i < 12; i++) {
      istream >> junk;
    }
    istream >> bw[index];
    istream >> iops[index];
    istream >> lat[index];
    index++;
  }
  ofstream oFile_bw;
  oFile_bw.open(argv[3]);
  for (int i = 0; i < size; i++) {
    oFile_bw << bw[i] << endl;
  }

  ofstream oFile_iops;
  oFile_iops.open(argv[4]);
  for (int i = 0; i < size; i++) {
    oFile_iops << iops[i] << endl;
  }

  ofstream oFile_lat;
  oFile_lat.open(argv[5]);
  for (int i = 0; i < size; i++) {
    oFile_lat << lat[i] << endl;
  }

  iFile.close();
  oFile_bw.close();
  oFile_iops.close();
  oFile_lat.close();
  return 0;
}