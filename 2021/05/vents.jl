# We have col major, AoC has row major, thus no transpose -- also, 1 index so +1
lines = reshape(parse.(Int, vcat(split.(vcat(split.(readlines(), " -> ")...), ",")...)), (4, :)) .+ 1
floormap = zeros(Int, (maximum(lines), maximum(lines)))

function fillmap!(floormap, x1, y1, x2, y2)
    if x1 != x2 && y1 != y2
        return
    end
    r = min(x1, x2):max(x1, x2)
    c = min(y1, y2):max(y1, y2)
    floormap[c, r] .+= 1
end

for col in eachcol(lines)
    fillmap!(floormap, col...)
end

println(sum(floormap .> 1))
