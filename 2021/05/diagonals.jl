# We have col major, AoC has row major, thus no transpose -- also, 1 index so +1
lines = reshape(parse.(Int, vcat(split.(vcat(split.(readlines(), " -> ")...), ",")...)), (4, :)) .+ 1
floormap = zeros(Int, (maximum(lines), maximum(lines)))

function fillmap!(floormap, x1, y1, x2, y2)
    # horizontal / vertical
    if x1 == x2 || y1 == y2
        r = min(x1, x2):max(x1, x2)
        c = min(y1, y2):max(y1, y2)
        floormap[c, r] .+= 1
        return
    end
    # diagonal
    if max(x1, x2) - min(x1, x2) == max(y1, y2) - min(y1, y2)
        coords = zip(x1:(-1)^(x1>x2):x2, y1:(-1)^(y1>y2):y2)
        for (r, c) in coords
            floormap[c, r] += 1
        end
    else
        println("INV ", x1, " ", y1, " -> ", x2, " ", y2)
    end

end

for col in eachcol(lines)
    fillmap!(floormap, col...)
end

# for row in eachrow(floormap)
#     println(row...)
# end
println(sum(floormap .> 1))
