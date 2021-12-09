lines = readlines()
numbers = parse.(Int, hcat(split.(lines[1], ",")))

boards = split.(lines[3:end])
boards = reshape(vcat(boards...), (5, 5, :))
boards = parse.(Int, boards)

println("Playing ", length(numbers), " numbers on ", size(boards)[3], " boards")

function playBingo(boards, numbers)
    winners = Set(1:size(boards)[3])
    marked = falses(size(boards))
    for number in numbers
        marked[boards .== number] .= true

        for board in winners
            bingo = all.(eachcol(marked[:, :, board])) .| all.(eachrow(marked[:, :, board]))

            if any(bingo)
                setdiff!(winners, [board])
                if length(winners) == 0
                    println("Last winning board: ", board)
                    winning = boards[:, :, board][.!marked[:, :, board]]
                    s = sum(winning)
                    println(s, " ", number)
                    return s * number
                end
            end
        end
    end
end


println(playBingo(boards, numbers))
