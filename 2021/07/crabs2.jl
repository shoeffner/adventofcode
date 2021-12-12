crabs = parse.(Int, vcat(split.(readline(), ",")))

positions = minimum(crabs):maximum(crabs)

dist = abs.(transpose(crabs) .- positions)
dist = (Int64).((dist .* dist .+ dist) ./ 2)

fuel = minimum(sum(dist, dims=2))
println(fuel)

