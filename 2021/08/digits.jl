l = length(filter(x -> x in [2, 4, 3, 7], length.(vcat(split.(vcat(split.(readlines(), " | ")...), " ")[2:2:end]...))))

println(l)
