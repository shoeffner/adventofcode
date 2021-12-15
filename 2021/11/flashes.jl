function main()
    lines = readlines()
    octos = transpose(reshape(parse.(Int, convert.(String, vcat(split.(lines, "")...))), (:, length(lines))))
    flashes = 0

    for step in 1:100
        flashed = zeros(Bool, size(octos))
        octos .+= 1

        tmpflash = -1

        maxc = size(octos, 2)
        maxr = size(octos, 1)
        while tmpflash != sum(flashed)
            newoctos = copy(octos)
            tmpflash = sum(flashed)
            for c in 1:maxc
                for r in 1:maxr
                    if octos[c, r] > 9 && !flashed[c, r]
                        flashed[c, r] = true
                        newoctos[max(c-1, 1):min(c+1, maxc), max(r-1, 1):min(r+1, maxr)] .+= 1
                    end
                end
            end
            octos = newoctos
        end
        octos[octos .> 9] .= 0

        flashes += sum(flashed)
    end

    println(flashes)
end


main()
