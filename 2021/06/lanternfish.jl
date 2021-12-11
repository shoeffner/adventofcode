days = 256
fish = zeros(Int, 9)

infish = parse.(Int, vcat(split.(readline(), ",")))
for f in infish
    fish[f+1] += 1
end


for i in 1:days
    spawners = popfirst!(fish)
    fish[7] += spawners
    push!(fish, spawners)
end

println(sum(fish))
