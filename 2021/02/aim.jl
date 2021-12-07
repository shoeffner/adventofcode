function process(lines)
    depth = 0
    fwd = 0
    aim = 0
    for row in eachrow(lines)
        dir = row[1][1]
        dist = parse(Int, row[1][2])
        if (dir == "forward")
            fwd += dist
            depth += dist * aim
        elseif (dir == "up")
            aim -= dist
        else
            aim += dist
        end
    end
    depth, fwd
end

lines = split.(readlines(), " ")
depth, fwd = process(lines)
print(depth * fwd)
