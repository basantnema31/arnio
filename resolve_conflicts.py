import sys

with open('cpp/src/csv_reader.cpp', 'r', encoding='utf-8') as f:
    content = f.read()

# Conflict 1
conflict1_start = content.find("<<<<<<< HEAD\n    bool getline(std::string& line, std::string& line_ending)")
conflict1_end = content.find(">>>>>>> upstream/main", conflict1_start) + len(">>>>>>> upstream/main\n")

if conflict1_start == -1 or conflict1_end == -1:
    print("Conflict 1 not found!")
    sys.exit(1)

resolved1 = """    bool getline(std::string& line, std::string& line_ending) {
        line.clear();
        line_ending = "\\n";

        while (true) {
            if (pos_ >= end_) {
                stream_.read(buffer_.data(), buffer_.size());
                end_ = stream_.gcount();
                pos_ = 0;
                if (end_ == 0) {
                    return !line.empty();
                }
            }

            size_t start = pos_;
            while (pos_ < end_) {
                char c = buffer_[pos_];
                if (c == '\\n' || c == '\\r' || c == '\\0') break;
                pos_++;
            }

            line.append(buffer_.data() + start, pos_ - start);

            if (pos_ < end_) {
                char c = buffer_[pos_];
                if (c == '\\0') {
                    throw std::runtime_error(
                        "CSV input contains NUL bytes and appears to be binary or corrupted");
                }

                if (c == '\\n') {
                    line_ending = "\\n";
                    pos_++;
                    return true;
                }

                if (c == '\\r') {
                    pos_++;
                    if (pos_ < end_) {
                        if (buffer_[pos_] == '\\n') {
                            pos_++;
                            line_ending = "\\r\\n";
                        } else {
                            line_ending = "\\r";
                        }
                    } else {
                        int next_c = stream_.peek();
                        if (next_c == '\\n') {
                            stream_.get();
                            line_ending = "\\r\\n";
                        } else {
                            line_ending = "\\r";
                        }
                    }
                    return true;
                }
            }
        }
    }

   private:
    std::istream& stream_;
    std::vector<char> buffer_;
    size_t pos_;
    size_t end_;
};

class RecordReader {
   public:
    explicit RecordReader(std::istream& stream) : reader_(stream) {
        record_.reserve(1024);
        line_.reserve(1024);
    }

    bool read(std::string& out_record) {
        size_t dummy = 0;
        return read(out_record, dummy);
    }

    bool read(std::string& out_record, size_t& line_number) {
        record_.clear();
        bool first = true;
        size_t record_start_line = line_number + 1;

        while (reader_.getline(line_, line_ending_)) {
            ++line_number;
            if (!first) {
                record_ += prev_line_ending_;
            }
            record_ += line_;
            prev_line_ending_ = line_ending_;
            first = false;

            if (record_complete(record_)) {
                out_record = record_;
                return true;
            }
        }

        if (!record_.empty() && !record_complete(record_)) {
            throw std::runtime_error("Unterminated quoted field starting at line " +
                                     std::to_string(record_start_line));
        }

        if (!record_.empty()) {
            out_record = record_;
            return true;
        }
        return false;
    }

   private:
    BufferedStreamReader reader_;
    std::string record_;
    std::string line_;
    std::string line_ending_;
    std::string prev_line_ending_;
};
"""

content = content[:conflict1_start] + resolved1 + content[conflict1_end:]

# Conflict 2
c2_start = content.find("<<<<<<< HEAD\n        while (skipped < to_skip && record_reader.read(line)) {")
c2_end = content.find(">>>>>>> upstream/main", c2_start) + len(">>>>>>> upstream/main\n")
if c2_start != -1:
    content = content[:c2_start] + "        while (skipped < to_skip && record_reader.read(line, line_number)) {\n" + content[c2_end:]

# Conflict 3
c3_start = content.find("<<<<<<< HEAD\n    if (config.has_header && record_reader.read(line)) {")
c3_end = content.find(">>>>>>> upstream/main", c3_start) + len(">>>>>>> upstream/main\n")
if c3_start != -1:
    content = content[:c3_start] + "    if (config.has_header && record_reader.read(line, line_number)) {\n" + content[c3_end:]

# Conflict 4
c4_start = content.find("<<<<<<< HEAD\n\n    std::vector<std::string> reusable_fields;")
c4_end = content.find(">>>>>>> upstream/main", c4_start) + len(">>>>>>> upstream/main\n")
if c4_start != -1:
    resolved4 = """
    std::vector<std::string> reusable_fields;
    if (expected_cols.has_value()) {
        reusable_fields.reserve(expected_cols.value());
    }

    while (record_reader.read(line, line_number)) {
"""
    content = content[:c4_start] + resolved4 + content[c4_end:]

with open('cpp/src/csv_reader.cpp', 'w', encoding='utf-8') as f:
    f.write(content)

print("Conflicts resolved!")
