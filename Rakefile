task :exec do
  system("python gargle.py")
end

task :default => [:clean, :exec]

task :clean do
  system("rm *.pyc")
end