require 'atk_toolbox'

system "ruby theme_generator.rb"
previous_process_finished_successfully = $?.success?
if previous_process_finished_successfully
    # push build
    if Console.args[0]
        system "project sync --message='#{Console.args[0]}'"
    else
        system "project sync"
    end
    
    if -"npm version patch"
        system "project synchronize --message='version bump'"
        puts "Publishing"
        system "vsce publish"
        puts "Finished Publishing"
    end
end