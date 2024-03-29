### A Pluto.jl notebook ###
# v0.19.32

using Markdown
using InteractiveUtils

# ╔═╡ d0042cdf-039f-4265-abeb-ffb7b836032a
using Test

# ╔═╡ e7e87b25-b103-4382-9b0c-67e17ed73313
function asdigit(number_str)
	if !(match(r"[0-9]", number_str) === nothing)
		return number_str
	end
	idx = findfirst(x -> x==number_str, ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"])
	"$idx"
end

# ╔═╡ 800870d1-1c9a-419a-a8fa-ee77ff5e551e
begin
	@test asdigit("one") == "1" == asdigit("1")
	@test asdigit("two") == "2"
	@test asdigit("three") == "3"
	@test asdigit("four") == "4"
	@test asdigit("five") == "5"
	@test asdigit("six") == "6"
	@test asdigit("seven") == "7"
	@test asdigit("eight") == "8"
	@test asdigit("nine") == "9"
	@test asdigit("0") == "0"
end

# ╔═╡ 18cbad78-b224-48c1-bc9a-256fa00f0dc8
function extract_number(line; words=false::Bool)
	if !words
		regex = r"[0-9]"
	else
		regex = r"([0-9]|one|two|three|four|five|six|seven|eight|nine)"
	end
	matches = collect(eachmatch(regex, line, overlap=true))
	parse(Int, asdigit(matches[begin].match) * asdigit(matches[end].match))
end

# ╔═╡ 8c373d2c-faca-4fd4-8141-4f9d2606a3b7
begin
	@test extract_number("12") == 12
	@test extract_number("a4") == 44
	@test extract_number("a1b2c3d") == 13
	@test extract_number("a1b2cthreed") == 12
	@test extract_number("a1b2cthreed", words=true) == 13
	@test extract_number("a1oneight", words=true) == 18
end

# ╔═╡ a1edcace-ad29-4154-8cc5-486dd3bace3f
function solve(content; words=false::Bool)
	sum(extract_number.(content, words=words))
end

# ╔═╡ 989bc191-db9f-43e1-b6f1-d592f65771b4
begin
	@test solve(readlines("example")) == 142
	@test solve(readlines("example2"), words=true) == 281
end

# ╔═╡ 22600232-a6dc-4722-8110-8f5ca1156879
solve(readlines("input"))

# ╔═╡ c7a058e3-b910-45d6-8dc1-ea6c680c4204
solve(readlines("input"), words=true)

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
# ╠═d0042cdf-039f-4265-abeb-ffb7b836032a
# ╠═e7e87b25-b103-4382-9b0c-67e17ed73313
# ╠═800870d1-1c9a-419a-a8fa-ee77ff5e551e
# ╠═18cbad78-b224-48c1-bc9a-256fa00f0dc8
# ╠═8c373d2c-faca-4fd4-8141-4f9d2606a3b7
# ╠═a1edcace-ad29-4154-8cc5-486dd3bace3f
# ╠═989bc191-db9f-43e1-b6f1-d592f65771b4
# ╠═22600232-a6dc-4722-8110-8f5ca1156879
# ╠═c7a058e3-b910-45d6-8dc1-ea6c680c4204
# ╟─00000000-0000-0000-0000-000000000001
# ╟─00000000-0000-0000-0000-000000000002
