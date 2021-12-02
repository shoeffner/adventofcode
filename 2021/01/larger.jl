depths = parse.(Int, readlines())
println(sum(depths[begin:end-1] .< depths[begin+1:end]))
