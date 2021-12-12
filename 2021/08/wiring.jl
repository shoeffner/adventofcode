function wiring_output(line)
    signaloutput = split(line, " | ")
    signal = convert.(String, split(signaloutput[1], " "))
    output = convert.(String, split(signaloutput[2], " "))

    lengths = length.(signal)
    extract_by_length = num -> signal[findall(lengths .== num)]

    # simple ones: always by length
    d1 = extract_by_length(2)[1]
    d4 = extract_by_length(4)[1]
    d7 = extract_by_length(3)[1]
    d8 = extract_by_length(7)[1]

    # 2, 3, and 5 have length 5
    d2 = ""
    d3 = ""
    d5 = ""
    candidates_235 = extract_by_length(5)

    for c in candidates_235
        if length(setdiff(Set(c), Set(d7), Set(d4))) == 2
            d2 = c
            break
        end
    end

    for c in candidates_235
        if c != d2 && length(setdiff(Set(c), Set(d7))) == 3
            d5 = c
            break
        end
    end

    for c in candidates_235
        if c != d5 && c != d2
            d3 = c
            break
        end
    end

    # 0, 6, and 9 have length 6
    d0 = ""
    d6 = ""
    d9 = ""
    candidates_069 = extract_by_length(6)

    for c in candidates_069
        if length(setdiff(Set(c), Set(d5))) == 2
            d0 = c
            break
        end
    end

    for c in candidates_069
        if c != d0
            if length(intersect(Set(c), Set(d1))) == 2
                d9 = c
            else
                d6 = c
            end
        end
    end

    # translate
    translate = [Set(d0), Set(d1), Set(d2), Set(d3), Set(d4), Set(d5), Set(d6), Set(d7), Set(d8), Set(d9)]

    factor = 1
    result = 0
    for o in output[end:-1:begin]
        so = Set(o)
        for i in 1:10
            if translate[i] == so
                result += (i - 1) * factor
                factor *= 10
                break
            end
        end
    end

    result
end


println(sum(map(wiring_output, readlines())))
