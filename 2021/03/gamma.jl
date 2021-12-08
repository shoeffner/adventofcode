lines = readlines()
width = length(lines[1])
lines = map(x -> reverse(digits(x, base=2, pad=width)), parse.(Int, lines, base=2))

mat = transpose(hcat(lines[:]...))

for col in eachcol(mat)
    if sum(col) == (Int)(length(col) / 2)
        println("PROBLEM for col ", col)
    end
end

gamma = [sum(col) > length(col) / 2 for col in eachcol(mat)]
epsilon = .!gamma

function asDec(bin)
    mapreduce((b, e) -> b*2^e, +, reverse(bin), Iterators.countfrom(0, 1))
end

gammadecimal = asDec(gamma)
epsilondecimal = asDec(epsilon)

println(gammadecimal, " * ", epsilondecimal, " = ")
println(gammadecimal * epsilondecimal)
