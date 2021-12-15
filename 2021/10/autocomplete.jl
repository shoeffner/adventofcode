function autocomplete(line)
    openclose = Dict('(' => ')', '[' => ']', '{' => '}', '<' => '>')
    stack = []
    for c in line
        if c in keys(openclose)
            push!(stack, openclose[c])
        else
            if pop!(stack) != c
                return []
            end
        end
    end
    return reverse(stack)
end


SCORES = Dict(')' => 1, ']' => 2, '}' => 3, '>' => 4)
function score(characters)
    total = 0
    for c in characters
        total *= 5
        total += SCORES[c]
    end
    return total
end


function main()
    scores = sort(filter(x -> x > 0, map(i -> score(i), map(autocomplete, readlines()))))
    println(scores[convert(Int, ceil(length(scores) / 2))])
end


main()

