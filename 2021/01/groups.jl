depths = parse.(Int, readlines())
depths = sum.(zip(depths[1:end-2], depths[2:end-1], depths[3:end]))
println(sum(depths[1:end-1] .< depths[2:end]))
