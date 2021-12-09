lines = readlines()
width = length(lines[1])
lines = map(x -> reverse(digits(x, base=2, pad=width)), parse.(Int, lines, base=2))

bits = BitArray(transpose(hcat(lines[:]...)))


function asDec(bin)
    mapreduce((b, e) -> b*2^e, +, reverse(bin), Iterators.countfrom(0, 1))
end


function getRating(bits, cmp)
    bitc = copy(bits)

    bitpos = 1
    while size(bitc)[1] > 1 && bitpos <= size(bitc)[2]
        col = bitc[:, bitpos]
        keep = cmp(sum(col), ceil(length(col) / 2))
        bitc = bitc[bitc[:, bitpos] .== keep, :]
        bitpos += 1
    end
    asDec(bitc)
end


oxygen = getRating(bits, >=)
co2scrubber = getRating(bits, <)

println(oxygen, " * ", co2scrubber, " =\n", oxygen * co2scrubber)
