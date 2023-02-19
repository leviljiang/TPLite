# Ground truth dataset

1. **TPL dependency**
   - [tpl_dep.csv](./tpl_dep.csv) contains the 2,150 tpl dependencies as the dataset in paper

   - continuous updating of the ground truth dataset for subsequent studies




2. **Binary SCA**

| Repo URL                                                     | Binary                   | Architecture      | #OSS                                                         |
| ------------------------------------------------------------ | ------------------------ | ----------------- | ------------------------------------------------------------ |
| https://github.com/ClickHouse/ClickHouse                     | clickhouse               | macOS/arm64       | clickhouse, jemalloc, avro, sqlite-amalgamation, yaml-cpp, magic_enum, zstd, arrow, libuv, brotli, re2, cyrus-sasl, fast_float, cppkafka, capnproto, libxml2, msgpack-c, xz, abseil-cpp, miniselect, replxx, dragonbox, double-conversion, lz4, xz, azure, simdjson, croaring, datasketches-cpp, fmt, grpc, protobuf, s2geometry, postgres, NuRaft, aws-sdk-cpp, AMQP-CPP, lemmagen-c, boringssl, snappy, zlib-ng, cctz, smhasher, Turbo-Base64, libstemmer_c, thrift, libfarmhash, poco, krb5, MetroHash, boost, cpp-driver, openldap, bzip2, librdkafka, h3, orc, llvm, libpqxx |
| https://github.com/continental/ecal                          | ecal_rec                 | macOS/arm64       | ecal, tinyxml, spdlog, fineftp-server, fmt                   |
| https://github.com/microsoft/Azure-Kinect-Sensor-SDK         | k4a.dll                  | windows/x86-64    | u'azure-c-shared-utility', u'Azure-Kinect-Sensor-SDK', u'cJSON', u'spdlog', u'libusb', u'fmt' |
| https://github.com/microsoft/Azure-Kinect-Sensor-SDK         | k4arecord                | windows/x86-64    | u'libebml', u'libjpeg-turbo', u'libmatroska', u'libyuv', u'Azure-Kinect-Sensor-SDK', u'azure-c-shared-utility', u'spdlog', u'libjpeg' |
| https://github.com/microsoft/Azure-Kinect-Sensor-SDK         | k4aviewer.exe            | windows/x86-64    | 'imgui', u'libsoundio', u'libjpeg-turbo', u'glfw', u'libyuv', u'Azure-Kinect-Sensor-SDK', u'libjpeg' |
| https://github.com/nesbox/TIC-80                             | tic80                    | windows/x86-64    | SDL, TIC-80, giflib, squirrel, zlib, curl, lua, lpeg, libpng, wren, blip-buf, dirent, zip, argparse, duktape-releases |
| https://github.com/TortoiseGit/TortoiseGit.git               | TortoiseGitMerge.exe     | windows/x86-64    | u'TortoiseGit', u'apr', u'resizablelib', u'simpleini', u'pcre2', u'editorconfig-core-c', u'apr-util' |
| https://github.com/TortoiseGit/TortoiseGit.git               | TortoiseGitProc.exe      | windows/x86-64    | u'TortoiseGit', u'ogdf', u'resizablelib', u'json', u'hunspell', u'simpleini' |
| https://gitlab.freedesktop.org/freetype/freetype.git         | freetype.dll             | windows/x86-64    | u'zlib', u'freetype'                                         |
| https://gitlab.freedesktop.org/freetype/freetype.git         | freetype250.dll          | windows/x86-64    | u'zlib', u'freetype'                                         |
| https://github.com/clamwin/clamav-win32.git                  | libclamavd.dll           | windows/x86-64    | u'libxml2', u'clamav', u'gnulib', u'tomsfastmath', u'clamav-win32', u'pcre2', u'json-c', u'libmspack', u'7z', u'bzip2', u'pthreads-win32', u'zlib', u'openssl' |
| https://github.com/vslavik/winsparkle.git                    | WinSparkle.dll           | windows/x86-64    | u'winsparkle', u'libexpat', u'wxWidgets', u'openssl'         |
| https://github.com/projectchrono/chrono.git                  | ChronoEngine.dll         | windows/x86-64    | u'rapidxml', u'filesystem', u'eigen', u'tinyobjloader', u'chrono' |
| https://github.com/XLabsProject/iw4x-client.git              | iw4x.dll                 | windows/x86-64    | u'protobuf', u'zlib', u'libtommath', u'libtomcrypt', u'iw4x-client', u'udis86', u'PDCurses', u'json11', u'mongoose' |
| https://github.com/nesbox/TIC-80.git                         | tic80.exe                | windows/x86-64    | u'SDL', u'TIC-80', u'giflib', u'squirrel', u'zlib', u'curl', u'lua', u'lpeg', u'libpng', u'wren', u'blip-buf', u'dirent', u'zip', u'argparse', u'duktape-releases' |
| https://github.com/grpc/grpc.git                             | grpc_csharp_ext.dll      | windows/x86-64    | u'boringssl', u'grpc', u'cares', u'abseil-cpp', u'zlib', u're2', u'upb' |
| https://github.com/petrockblog/ControlBlockService2.git      | controlblock             | Ubuntu/i386       | ControlBlockService2, jsoncpp, LIO, plog, fmt, libmcp23s17, gcc, glibc |
| [git://github.com/powturbo/TurboBench.git](git://github.com/powturbo/TurboBench.git) | turbobench               | Arch Linux/x86_64 | FastLZ, libbsc, zlib, zopfli, zpaq, lzfse, lizard, lz4, libdeflate, pysap, fast-lzma2, lzma, lzsa, glibc, gcc, lzham_codec_devel, Turbo-Range-Coder, brotli, lzo, zstd, Turbo-Run-Length-Encoding, bzip2, glza, lzlib, quicklz, libsais, xxHash, facebook_folly, FiniteStateEntropy, TurboBench |
| https://github.com/Tencent/tendis.git                        | tendisplus               | Ubuntu/x86_64     | glog, snappy, lz4, jemalloc, asio, tendis, rocksdb, gcc, glibc, rapidjson, lua, lua-cmsgpack, smhasher |
| https://github.com/kvrockslabs/kvrocks.git                   | kvrocks                  | Ubuntu/i386       | glog, rocksdb, libevent, jemalloc, kvrocks, gcc, glibc, lua, chrono |
| https://github.com/apache/incubator-pagespeed-mod.git        | pagespeed_automatic_test | Arch Linux/x86_64 | brotli, apr-util, re2, libpng, hiredis, apr, libwebp, grpc, protobuf, sparsehash, jsoncpp, googletest, googlemock, zlib, giflib-mirror, incubator-pagespeed-mod, glibc, gcc, boringssl, incubator-pagespeed-icu, base, libjpeg_turbo, google-url, src, incubator-pagespeed-drp, incubator-pagespeed-optipng, cpp-base64, android_libutf, rdestl, redis, apatch_serf, openbsd, netlib_fp, nspr |
| https://github.com/bytedance/terarkdb.git                    | db_bench                 | Arch Linux/x86_64 | zstd, zlib, snappy, lz4, jemalloc, gflags, glibc, gcc, zenfs, bzip2, rocksdb, googletest, xxHash, FiniteStateEntropy, terarkdb |
| https://github.com/jupp0r/prometheus-cpp.git                 | prometheus_test          | Arch Linux/x86_64 | googletest, prometheus-cpp, glibc, gcc, protobuf             |
| https://github.com/realnc/dosbox-core.git                    | dosbox_core_libretro.so  | Arch Linux/x86_64 | flac, opus, fluidsynth, dosbox-core, glibc, gcc, libretro-common, libsndfile, SDL-1.2, libffi, SDL_audiolib, libinstpatch, munt, vorbis, fmt, SDL_net, ogg, dr_libs, opus-tools |
| https://github.com/SmartThingsCommunity/st-device-sdk-c.git  | example                  | Ubuntu/i386       | libsodium, mbedtls, st-device-sdk-c, glibc, gcc, cJSON       |
| https://github.com/yuzu-emu/yuzu-mainline.git                | yuzu-cmd                 | Arch Linux/x86_64 | inih, xbyak, opus, SDL, cpp-httplib, yuzu-mainline, glibc, gcc, dynarmic, ext-soundtouch, mbedtls, sirit, cubeb, microprofile, boost_crc, fmt, nlohmann, wayland, hidapi, expected, Open-Source-AHRS-With-x-IMU, dolphin, citra, cityhash |
| https://github.com/marlinprotocol/OpenWeaver.git             | eth_sc                   | Arch Linux/x86_64 | boost, libsodium, spdlog, libuv, cryptopp, structopt, rapidjson, abseil-cpp, glibc, gcc, secp256k1, fmt, magic_enum, OpenWeaver |
| https://github.com/matanui159/ReplaySorcery.git              | replay-sorcery           | Arch Linux/x86_64 | libjpeg-turbo, fdk-aac, ReplaySorcery, glibc, gcc, sdl2-audio-monitor, x264, libbacktrace, minimp4, yuv2rgb |
| https://github.com/hyrise/hyrise.git                         | hyriseSystemTest         | Ubuntu/x86_64     | cxxopts, googletest, robin-hood-hashing, hyrise, tpcds-kit, libpqxx, json, tbb, tpch-dbgen, boost_* * 31 likes boost_range, boost_graph... |
| https://github.com/nanocurrency/nano-node.git                | nano_node                | Ubuntu/x86_64     | miniupnp, lmdb, cryptopp, flatbuffers, rocksdb, nano-node, boost, gcc, glibc, cpptoml, phc-winner-argon2, crc32c, xxHash, zstd, boost_* * 45 likes boost_preprocessor, boost_variant... |

*The rest binary files please refer to [archlinux packages](https://archlinux.org/packages/)
