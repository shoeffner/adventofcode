function findillegal(line)
    openclose = Dict('(' => ')', '[' => ']', '{' => '}', '<' => '>')
    stack = []
    for c in line
        if c in keys(openclose)
            push!(stack, openclose[c])
        else
            if pop!(stack) != c
                return c
            end
        end
    end
    return nothing
end


function main()
    scores = Dict(nothing => 0, ')' => 3, ']' => 57, '}' => 1197, '>' => 25137)
    println(sum(map(i -> scores[i], map(findillegal, readlines()))))
end


main()
