function readgraph()
    x = split.(vcat(readlines()), "-")
    edges = hcat([convert.(String, [f, t]) for (f, t) in x]...)
    from = vcat(edges[1, :], edges[2, :])
    to = vcat(edges[2, :], edges[1, :])
    vertices = Set(edges)
    return from, to, vertices
end


function followpath(node, goal, from, to, available, singleuse, path=nothing, paths=nothing)
    if paths == nothing
        paths = []
    end

    if path == nothing
        path = []
    else
        path = copy(path)
    end
    push!(path, node)
    if node == goal
        # println("Goal reached: ", path)
        push!(paths, path)
        return
    end

    ac = copy(available)
    if node in singleuse
        pop!(ac, node)
    end
    possible = to[from .== node]

    # println("Node: ", node, " Possible: ", possible, " Path: ", path, " Available: ", ac)

    if length(possible) == 0
        return
    end

    for next in possible
        if next in ac
            followpath(next, goal, from, to, ac, singleuse, path, paths)
        end
    end

    return paths
end


function collectpaths()
    from, to, vertices = readgraph()
    singleuse = Set(["start", "end"])
    for x in vertices
        if islowercase(x[1])
            push!(singleuse, x)
        end
    end
    followpath("start", "end", from, to, vertices, singleuse)
end


function main()
    println(length(collectpaths()))
end


main()

# println(to[from .== "start"])
