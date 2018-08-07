#!/bin/bash
set -eu

function redirect
{
	local from_dir=$1
	local to_file=$2
	local to_url="$to_file"

	mkdir -p $from_dir

	cat > $from_dir/index.html <<- EOM
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0; url=$to_url">
        <script type="text/javascript">
            window.location.href = "$to_url"
        </script>
        <title>Page Redirection</title>
    </head>
    <body>
        If you are not redirected automatically, follow this <a href='$to_url'>link to the article.</a>.
    </body>
</html>
	EOM
}

# Redirect paths from old squarespace website:
redirect blog/2017/9/24/fitting-a-plane-to-noisy-points-in-3d             ../../../../../2017_09_25_plane_from_points_2.html
redirect blog/2017/7/9/hitting-the-bullseye-adventures-in-computer-vision ../../../../../2017_07_19_hitting_the_bullseye.html
redirect blog/2017/6/1/float-or-double                                    ../../../../../2017_06_01_float_or_double.html
redirect blog/2017/4/23/abstractions-a-cautionary-tale                    ../../../../../2017_04_23_abstractions.html
redirect blog/2016/11/22/the-unfixable-bug                                ../../../../../2016_11_22_unfixable_bug.html
redirect blog/2016/10/12/stick-to-utf-8-and-these-three-character-sets    ../../../../../2016_10_12_character_sets.html
redirect blog/2016/8/28/designing-a-fast-hash-table                       ../../../../../2016_08_28_hash_table.html
redirect blog/2016/3/20/coroutines-for-games                              ../../../../../2016_03_20_coroutines.html
redirect blog/2016/2/28/error-context-better-logging-with                 ../../../../../2016_02_28_error_context.html
redirect blog/2016/1/25/configuru                                         ../../../../../2016_01_26_configuru.html
redirect blog/2016/1/25/you-deserve-great-error-messages                  ../../../../../2016_01_25_error_messages.html
redirect blog/2015/12/6/the-fastest-code-is-the-code-that-never-runs      ../../../../../2015_12_06_gauntlet.html
redirect blog/loguru                                                      ../../2015_11_07_loguru.html
redirect blog/2015/3/2/plane-from-points                                  ../../../../../2015_03_04_plane_from_points.html
redirect blog/2015/2/9/the-myth-of-ram-part-iv                            ../../../../../2015_02_09_myth_of_ram_4.html
redirect blog/2015/2/5/what-a-difference-a-function-makes                 ../../../../../2015_02_05_remap.html
redirect blog/2014/12/7/lessons-after-a-year-with-lua                     ../../../../../2014_12_07_lessons_from_lua.html
redirect blog/2014/5/10/responsiveness                                    ../../../../../2014_05_13_responsiveness.html
redirect blog/2014/5/6/type-safe-identifiers-in-c                         ../../../../../2014_05_06_type_safe_handles.html
redirect blog/2014/4/29/the-myth-of-ram-part-iii                          ../../../../../2014_04_29_myth_of_ram_3.html
redirect blog/2014/4/28/the-myth-of-ram-part-ii                           ../../../../../2014_04_28_myth_of_ram_2.html
redirect blog/2014/4/21/the-myth-of-ram-part-i                            ../../../../../2014_04_21_myth_of_ram_1.md.html
