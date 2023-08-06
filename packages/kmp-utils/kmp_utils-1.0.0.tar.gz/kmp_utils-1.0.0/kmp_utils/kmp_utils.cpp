#include <string>
#include <vector>
#include <iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "kmp_utils.h"

PYBIND11_MODULE(example, m) {
    m.def("find_all", &kmp::find_all, "Find all occurrences of t in s reading left to right");
    m.def("find_all_left", &kmp::find_all_left, "Find all occurrences of t in s reading right to left");
    m.def("split", &kmp::split, "Split string s by delimiter t");
    m.def("get_next_left", &kmp::get_next_left, "get next right occurence of t in s starting from index i");
    m.def("get_next_right", &kmp::get_next_right, "get next left occurence of t in s starting from index i");
}

std::vector<int> kmp::find_all(std::string & s, std::string & t) {
  std::vector<int> result;
  std::vector<int> pt = kmp::compute_prefix_table(t);
  int index = kmp::find_next(s, t, 0, pt);
  while (index != -1) {
    result.push_back(index);
    index = kmp::find_next(s, t, index + t.length(), pt);
  }
  return result;
}

std::vector<int> kmp::find_all_v2(std::string & s, std::string & t) {
  std::vector<int> result;
  std::vector<int> pt = kmp::compute_prefix_table(t);
  int index = kmp::find_next(s, t, 0, pt);
  int n = s.length();
  int m = t.length();
  while (index != -1) {
    result.push_back(index);
    if (n - index < m) {break;}
    int i = index + m;
    int j = 0;
    index = -1;
    while (i < n) {
      if (s.at(i) == t.at(j)) {
        i++;
        j++;
        if (j == m) {
          index = i-m;
          break;
        }
        continue;
      }
      while (j > 0 && t.at(j) != s.at(i)) {
        j = pt[j-1];
      }
      if (j == 0 && t.at(j) != s.at(i)) {
        i++;
      }
    }
  }
  return result;
}

std::vector<std::string> kmp::split(std::string & s, std::string & t) {
  std::vector<std::string> result;
  std::vector<int> pt = kmp::compute_prefix_table(t);
  int index = kmp::find_next(s, t, 0, pt);
  int start = 0;
  while (index != -1) {
    result.push_back(s.substr(start, index - start));
    start = index + t.length();
    index = kmp::find_next(s, t, index + t.length(), pt);
  }
  // append last occurence
  result.push_back(s.substr(start, s.length() - start));
  return result;
}

int kmp::find_next(std::string & s, std::string & t, int index, std::vector<int> pt) {
  int n = s.length();
  int m = t.length();
  if (n < m) {
    return -1;
  }
  int i = index;
  int j = 0;
  while (i < n) {
    if (s.at(i) == t.at(j)) {
      i++;
      j++;
      if (j == m) {
        return i-m;
      }
      continue;
    }
    while (j > 0 && t.at(j) != s.at(i)) {
      j = pt[j-1];
    }
    if (j == 0 && t.at(j) != s.at(i)) {
      i++;
    }
  }
  return -1;
}

std::vector<int> kmp::compute_prefix_table(std::string & pattern) {
  int m = pattern.length();
  std::vector<int> prefix_table(m);
  int j = 0;
  for (int i = 1; i < m; i++) {
    while (j > 0 && pattern.at(j) != pattern.at(i)) {
      j = prefix_table[j-1];
    }
    if (pattern.at(j) == pattern.at(i)) {
      j++;
    }
    prefix_table[i] = j;
  }
  return prefix_table;
}

std::vector<int> kmp::compute_suffix_table(std::string & pattern) {
  int m = pattern.length();
  std::vector<int> prefix_table(m);
  int j = 0;
  for (int i = 1; i < m; i++) {
    while (j > 0 && pattern.at(m-j-1) != pattern.at(m-i-1)) {
      j = prefix_table[j-1];
    }
    if (pattern.at(m-j-1) == pattern.at(m-i-1)) {
      j++;
    }
    prefix_table[i] = j;
  }
  std::vector<int> suffix_table(m);
  for (int i = 0; i < m; i++) {
    suffix_table[m-i-1] = prefix_table[i];
  }

  return suffix_table;
}

int kmp::find_next_left(std::string & s, std::string & t, int index, std::vector<int> st) {
  int n = s.length();
  int m = t.length();
  if (n < m) {
    return -1;
  }
  int i = index;
  int j = m - 1;
  while (i >= 0) {
    if (s.at(i) == t.at(j)) {
      i--;
      j--;
      if (j == -1) {
        return i+1;
      }
      continue;
    }
    while (j < m - 1 && t.at(j) != s.at(i)) {
      j = m - st[j+1] - 1;
    }
    if (j == m - 1 && t.at(j) != s.at(i)) {
      i--;
    }
  }
  return -1;
}

int kmp::get_next_left(std::string & s, int i, std::string & t) {
  std::vector<int> st = kmp::compute_suffix_table(t);
  return kmp::find_next_left(s, t, i, st);
}

std::vector<int> kmp::find_all_left(std::string & s, std::string & t) {
  std::vector<int> result;
  std::vector<int> st = kmp::compute_suffix_table(t);
  int index = kmp::find_next_left(s, t, s.length() - 1, st);
  while (index != -1) {
    result.push_back(index);
    index = kmp::find_next_left(s, t, index - 1, st);
  }
  return result;
}

int kmp::get_next_right(std::string & s, int i, std::string & t) {
  std::vector<int> pt = kmp::compute_prefix_table(t);
  return kmp::find_next(s, t, i, pt);
}

std::string& kmp::ltrim(std::string& s, const char * t) {
  s.erase(0, s.find_first_not_of(t));
  return s;
}

std::string& kmp::rtrim(std::string& s, const char * t) {
  s.erase(s.find_last_not_of(t) + 1);
  return s;
}

std::string& kmp::trim(std::string& s) {
  const char * t = " \t\n\r\f\v";
  return kmp::ltrim(kmp::rtrim(s, t), t);
}

std::string kmp::join(std::vector<std::string>& v, std::string& delim) {
  std::string result;
  for (int i = 0; i < v.size(); i++) {
    result += v[i];
    if (i == v.size() - 1) { break; }
    result += delim;
  }
  return result;
}

std::string kmp::replace_all(std::string& s, std::string& p, std::string& t) {
  std::vector<std::string> v = kmp::split(s, p);
  return kmp::join(v, t);
}

std::vector<std::string> kmp::deserialize_list(std::string& v) {
  std::string sw = "\"";
  std::string sw1 = "\\\"";
  std::string boundary = "a\"";
  std::vector<std::string> result;
  std::vector<std::string> t1 = kmp::split(v, boundary);
  for (int i = 0; i < t1.size(); i++) {
    std::string s = kmp::replace_all(t1[i], sw1, sw);
    result.push_back(s);
  }
  return result;
}

std::string kmp::serialize_list(std::vector<std::string>& v) {
  std::string sw = "\"";
  std::string sw1 = "\\\"";
  std::string boundary = "a\"";
  std::string result = "";
  for (int i = 0; i < v.size(); i++) {
    result += kmp::replace_all(v[i], sw, sw1);
    if (i == v.size() - 1) { break; }
    result += boundary;
  }
  return result;
}

bool in_string(std::string& s, char c) {
  for (int i = 0; i < s.length(); i++) {
    if (s[i] == c) { return true; }
  }
  return false;
}

std::vector<std::string> kmp::sent_tokenize(std::string& s) {
  std::vector<std::string> result;
  std::string st = "";
  std::string tokens = ".;\n";
  for (int i = 0; i < s.length(); i++) {
    if (in_string(tokens, s[i])) {
      result.push_back(st);
      st = "";
    }
    st += s[i];
  }
  if (st.length() > 0) { result.push_back(st); }
  return result;
}

std::vector<std::string> kmp::word_tokenize(std::string& s) {
  std::vector<std::string> result;
  std::string st = "";
  std::string tokens = ", ";
  for (int i = 0; i < s.length(); i++) {
    if (in_string(tokens, s[i])) {
      result.push_back(st);
      st = "";
    }
    st += s[i];
  }
  if (st.length() > 0) { result.push_back(st); }
  return result;
}
