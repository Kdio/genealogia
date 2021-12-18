### bash
# $>cd folder
# $>IFS=$'\n'; set -f
# $>for f in $(find * -name '*.htm' -or -name '*.html'); do iconv -f CP1252 -t UTF-8 "$f" -o "$f"; done
# $>unset IFS; set +f

require 'nokogiri'

# Folder to cleanup from command line
return if ARGV.empty?
folder = ARGV.join(' ')
return if folder.empty? || !File.directory?(folder)

def read_text_file(filename)
  # puts filename
  Nokogiri::HTML.parse(
    remove_spaces(
      File.read(filename)
        .tr("\r\n", ' ')
        .gsub(/<[^>]*>/ui,'')
        .gsub("\"","'")
        .gsub('&nbsp;', ' ')
    )
  ).text
end

def remove_spaces(string)
  while string.include?('  ') do
    string = string.gsub('  ', ' ')
  end
  string
end

filenames = Dir.glob("#{folder}/**/*")

filenames.each do |filename|
  if filename.include?('.htm')
    File.write(filename, read_text_file(filename))
  else
    File.delete(filename) if File.file?(filename)
  end
end
