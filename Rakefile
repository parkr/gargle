task :exec do
  system("python gargle.py")
end

task :default => [:clean, :exec]

task :install do
  system("easy_install lxml")
  system("easy_install progressbar")
  # numpy
  #some error like this: "ImportError: No module named numpy"
end

task :clean do
  system("rm *.pyc")
end