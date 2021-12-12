crabs = parse.(Int, vcat(split.(readline(), ",")))

positions = minimum(crabs):maximum(crabs)

fuel = minimum(sum(abs.(transpose(crabs) .- positions), dims=2))
println(fuel)
