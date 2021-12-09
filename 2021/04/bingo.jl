lines = readlines()
numbers = parse.(Int, hcat(split.(lines[1], ",")))

boards = split.(lines[3:end])
boards = reshape(vcat(boards...), (5, 5, :))
boards = parse.(Int, boards)

println("Playing ", length(numbers), " numbers on ", size(boards)[3], " boards")

function playBingo(boards, numbers)
    marked = falses(size(boards))
    for number in numbers
        marked[boards .== number] .= true

        for board in 1:size(marked)[3]
            bingo = all.(eachcol(marked[:, :, board])) .| all.(eachrow(marked[:, :, board]))

            if any(bingo)
                println("Winning board: ", board)
                winning = boards[:, :, board][.!marked[:, :, board]]
                s = sum(winning)
                println(s, " ", number)
                return s * number
            end
        end
    end
end


println(playBingo(boards, numbers))
