### A Pluto.jl notebook ###
# v0.19.32

using Markdown
using InteractiveUtils

# ╔═╡ fc792c55-2f6a-4015-afa5-1bdb85fd40b2
using Test

# ╔═╡ 4beaa47a-bad9-4fbb-9ac1-02d8bfee3806
function parsecolor(colstr)
	s = split(strip(colstr), " ")
	String(s[2]), parse(Int, s[1])
end

# ╔═╡ 717ee40f-ab37-497c-9288-4929ab2da27b
function drawcolors(draw)
	Dict(parsecolor.(eachsplit(draw, ",")))
end

# ╔═╡ 35133b42-a9fc-48ff-9d89-09aaa368f013
begin
	@test drawcolors("3 blue, 4 red") == Dict("blue"=>3, "red"=>4)
	@test drawcolors("1 red, 2 green, 6 blue") == Dict("red"=>1, "green"=>2, "blue"=>6)
	@test drawcolors("2 blue") == Dict("blue"=>2)
end

# ╔═╡ 988d0a31-9b69-4b57-bc3b-258a8b7137d0
function exceeds(draw, maxcubes)
	for color in keys(maxcubes)
		numcubes = get(draw, color, 0)
		if numcubes > maxcubes[color]
			return true
		end
	end
	return false
end

# ╔═╡ 76982840-92ce-41f3-ad22-75226936f8c5
begin
	@test exceeds(Dict("blue" => 3, "red" => 4), Dict("blue" => 3, "red" => 2))
	@test !exceeds(Dict("blue"=>3, "green" => 4), Dict("blue" => 3, "red" => 2))
	@test exceeds(Dict("blue"=> 5, "red" => 4), Dict("blue" => 3, "red" => 2))
	@test !exceeds(Dict("blue"=>3), Dict("blue" => 4, "red" => 2))
	@test !exceeds(Dict("blue"=>3), Dict("green" => 4))
end

# ╔═╡ 8cffc78f-13f2-4907-8153-bbc07c1d3e68
function possible(game; maxcubes)
	draws = split(game, ":")[end]
	for colors in drawcolors.(eachsplit(draws, ";"))
		if exceeds(colors, maxcubes)
			return false
		end
	end
	true
end

# ╔═╡ bd1256ee-9324-43f0-aa90-a7ccee344aa7
begin
	@test !possible("3 blue, 4 red"; maxcubes=Dict("blue" => 3, "red" => 2))
	@test possible("3 blue, 4 green"; maxcubes=Dict("blue" => 3, "red" => 2))
	@test !possible("5 blue, 4 red"; maxcubes=Dict("blue" => 3, "red" => 2))
	@test possible("3 blue"; maxcubes=Dict("blue" => 4, "red" => 2))
	@test possible("3 blue"; maxcubes=Dict("green" => 4))
end

# ╔═╡ 8558d4b9-a128-4b90-ba5f-fc63460e9e33
function power(game)
	draws = split(game, ":")[end]
	result = Dict("red" => 0, "green" => 0, "blue" => 0)
	for draw in drawcolors.(eachsplit(draws, ";"))
		for color in keys(result)
			result[color] = max(result[color], get(draw, color, 0))
		end
	end
	reduce(*, values(result))
end

# ╔═╡ c24daa28-9117-11ee-346b-71590579ec33
function solve(input; variant::Bool=false)
	if !variant
		return sum(findall(possible.(input; maxcubes=Dict("red" => 12, "green" => 13, "blue" => 14))))
	end
	sum(power.(input))
end

# ╔═╡ eab81b76-56fe-4b22-b2a4-a3d5e38f009a
begin
	@test solve(readlines("example")) == 8
	@test solve(readlines("example"), variant=true) == 2286
end

# ╔═╡ ec5e6007-2611-40c6-985c-6258a91d863d
solve(readlines("input"))

# ╔═╡ 73d68e60-3f70-429e-a9ce-e4204cf39f2a
solve(readlines("input"), variant=true)

# ╔═╡ 00000000-0000-0000-0000-000000000001
PLUTO_PROJECT_TOML_CONTENTS = """
[deps]
Test = "8dfed614-e22c-5e08-85e1-65c5234f0b40"
"""

# ╔═╡ 00000000-0000-0000-0000-000000000002
PLUTO_MANIFEST_TOML_CONTENTS = """
# This file is machine-generated - editing it directly is not advised

julia_version = "1.9.4"
manifest_format = "2.0"
project_hash = "71d91126b5a1fb1020e1098d9d492de2a4438fd2"

[[deps.Base64]]
uuid = "2a0f44e3-6c83-55bd-87e4-b1978d98bd5f"

[[deps.InteractiveUtils]]
deps = ["Markdown"]
uuid = "b77e0a4c-d291-57a0-90e8-8db25a27a240"

[[deps.Logging]]
uuid = "56ddb016-857b-54e1-b83d-db4d58db5568"

[[deps.Markdown]]
deps = ["Base64"]
uuid = "d6f4376e-aef5-505a-96c1-9c027394607a"

[[deps.Random]]
deps = ["SHA", "Serialization"]
uuid = "9a3f8284-a2c9-5f02-9a11-845980a1fd5c"

[[deps.SHA]]
uuid = "ea8e919c-243c-51af-8825-aaa63cd721ce"
version = "0.7.0"

[[deps.Serialization]]
uuid = "9e88b42a-f829-5b0c-bbe9-9e923198166b"

[[deps.Test]]
deps = ["InteractiveUtils", "Logging", "Random", "Serialization"]
uuid = "8dfed614-e22c-5e08-85e1-65c5234f0b40"
"""

# ╔═╡ Cell order:
# ╠═fc792c55-2f6a-4015-afa5-1bdb85fd40b2
# ╠═4beaa47a-bad9-4fbb-9ac1-02d8bfee3806
# ╠═717ee40f-ab37-497c-9288-4929ab2da27b
# ╠═35133b42-a9fc-48ff-9d89-09aaa368f013
# ╠═988d0a31-9b69-4b57-bc3b-258a8b7137d0
# ╠═76982840-92ce-41f3-ad22-75226936f8c5
# ╠═8cffc78f-13f2-4907-8153-bbc07c1d3e68
# ╠═bd1256ee-9324-43f0-aa90-a7ccee344aa7
# ╠═8558d4b9-a128-4b90-ba5f-fc63460e9e33
# ╠═c24daa28-9117-11ee-346b-71590579ec33
# ╠═eab81b76-56fe-4b22-b2a4-a3d5e38f009a
# ╠═ec5e6007-2611-40c6-985c-6258a91d863d
# ╠═73d68e60-3f70-429e-a9ce-e4204cf39f2a
# ╟─00000000-0000-0000-0000-000000000001
# ╟─00000000-0000-0000-0000-000000000002
