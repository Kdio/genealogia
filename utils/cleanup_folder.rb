require 'nokogiri'

# Folder to cleanup from command line
return if ARGV.empty?
folder = ARGV.join(' ')
return if folder.empty? || !File.directory?(folder)

def read_text_file(filename)
  Nokogiri::HTML.parse(
    remove_spaces(
      File.read(filename, encoding: 'ISO-8859-1:UTF-8')
        .tr("\r\n", ' ')
        .gsub(/<[^>]*>/ui,'')
        .gsub('&nbsp;', ' ')
        # .delete("^\u{0000}-\u{007F}")
    )
  ).text.encode('UTF-8')

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
