/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "2.0.0a10/advanced/export-and-require.html",
    "revision": "15131978308630f968e4a27e66a04b9d"
  },
  {
    "url": "2.0.0a10/advanced/index.html",
    "revision": "0b5dcfccd511cfd95d9e5e2890f4c33a"
  },
  {
    "url": "2.0.0a10/advanced/overloaded-handlers.html",
    "revision": "f7cc6c3d40bfc75190d122d36db7e811"
  },
  {
    "url": "2.0.0a10/advanced/permission.html",
    "revision": "410f89a240946dc54c71ce73603b35dc"
  },
  {
    "url": "2.0.0a10/advanced/publish-plugin.html",
    "revision": "1f4ce0d3e658675c1053ea344acebfdc"
  },
  {
    "url": "2.0.0a10/advanced/runtime-hook.html",
    "revision": "b4cc73a8d4b70acb40292bee1df4d546"
  },
  {
    "url": "2.0.0a10/advanced/scheduler.html",
    "revision": "701f6c2a6a40997e58e39bda52801240"
  },
  {
    "url": "2.0.0a10/api/adapters/cqhttp.html",
    "revision": "f76c5693ee948e5e74d8f3c27a810165"
  },
  {
    "url": "2.0.0a10/api/adapters/ding.html",
    "revision": "c2d4ccf8807717161942922fdd48c27d"
  },
  {
    "url": "2.0.0a10/api/adapters/index.html",
    "revision": "0da24a5eb71cbdc9b750b5107d7a26fb"
  },
  {
    "url": "2.0.0a10/api/adapters/mirai.html",
    "revision": "c3913755d0fdc0752964bc1f54001684"
  },
  {
    "url": "2.0.0a10/api/config.html",
    "revision": "dd06afbec883ecd3d00d4c0669802a75"
  },
  {
    "url": "2.0.0a10/api/drivers/fastapi.html",
    "revision": "fe68d30e3ff5c0cee82130242d9c2136"
  },
  {
    "url": "2.0.0a10/api/drivers/index.html",
    "revision": "d80938024c91b5e997a9f360c5cc5d54"
  },
  {
    "url": "2.0.0a10/api/drivers/quart.html",
    "revision": "425c859f48911ab9601645bf10c90b68"
  },
  {
    "url": "2.0.0a10/api/exception.html",
    "revision": "6b3360d0f4a7b83c6c07ed52aac3379c"
  },
  {
    "url": "2.0.0a10/api/index.html",
    "revision": "bfaea1eca977df2361b3a7d2a42ba5c0"
  },
  {
    "url": "2.0.0a10/api/log.html",
    "revision": "0ff4cfdcdbbcf20f08a936d3b1b0bac4"
  },
  {
    "url": "2.0.0a10/api/matcher.html",
    "revision": "49fd6e0f5f5e915b328143f240bbf2e2"
  },
  {
    "url": "2.0.0a10/api/message.html",
    "revision": "d395adc067737b65f650e7d5898ac623"
  },
  {
    "url": "2.0.0a10/api/nonebot.html",
    "revision": "b069c821cc734fe91d86cfd4819376c1"
  },
  {
    "url": "2.0.0a10/api/permission.html",
    "revision": "ea1f01b10cf13899680b6970c66cbf5a"
  },
  {
    "url": "2.0.0a10/api/plugin.html",
    "revision": "9698af78da4850cb38aea9b2d803e626"
  },
  {
    "url": "2.0.0a10/api/rule.html",
    "revision": "857594e11a2177222f200256b57f9a49"
  },
  {
    "url": "2.0.0a10/api/typing.html",
    "revision": "0ea9eb2a705af196b8560f9d0587e3dd"
  },
  {
    "url": "2.0.0a10/api/utils.html",
    "revision": "677abf3b10544372771e2cf8f7a4eeba"
  },
  {
    "url": "2.0.0a10/guide/basic-configuration.html",
    "revision": "f378ae9c3619594a693f690042e1f4bc"
  },
  {
    "url": "2.0.0a10/guide/cqhttp-guide.html",
    "revision": "326e3a2bf811e649de0b428b04f80f72"
  },
  {
    "url": "2.0.0a10/guide/creating-a-handler.html",
    "revision": "515f2e99a3f230dd33893fa81e935397"
  },
  {
    "url": "2.0.0a10/guide/creating-a-matcher.html",
    "revision": "6058d4d7a6ba734c553c86f97b110477"
  },
  {
    "url": "2.0.0a10/guide/creating-a-plugin.html",
    "revision": "9ff57aa1880e13b6b9d3c466b8fc6a49"
  },
  {
    "url": "2.0.0a10/guide/creating-a-project.html",
    "revision": "824800b4e54a9db744630f1ad3a2a30b"
  },
  {
    "url": "2.0.0a10/guide/ding-guide.html",
    "revision": "7a3066a72dba8189dd1707c4946ce86d"
  },
  {
    "url": "2.0.0a10/guide/end-or-start.html",
    "revision": "3e7babeb0dca020e6e626735ea185955"
  },
  {
    "url": "2.0.0a10/guide/getting-started.html",
    "revision": "9da0423eedf780bf9dcf625c55722328"
  },
  {
    "url": "2.0.0a10/guide/index.html",
    "revision": "69cb6dbcad12c6a6247336532e0f490e"
  },
  {
    "url": "2.0.0a10/guide/installation.html",
    "revision": "95abf9ed8b16d8ef92386ee38cf7e1a2"
  },
  {
    "url": "2.0.0a10/guide/loading-a-plugin.html",
    "revision": "aa82ef7e37d66df1b7b75ea5ea2eadc6"
  },
  {
    "url": "2.0.0a10/guide/mirai-guide.html",
    "revision": "f91bff49cf5ed3b576536ff6d79bb52f"
  },
  {
    "url": "2.0.0a10/index.html",
    "revision": "6e3e9b036dde9794c04a69eb2153660d"
  },
  {
    "url": "2.0.0a13.post1/advanced/export-and-require.html",
    "revision": "8a766d7f57605c995ebd8a94460ba148"
  },
  {
    "url": "2.0.0a13.post1/advanced/index.html",
    "revision": "e687fd2c96e6d266fdb33e5ab819f936"
  },
  {
    "url": "2.0.0a13.post1/advanced/overloaded-handlers.html",
    "revision": "b9f771fb0613945e8bcb61093f33af82"
  },
  {
    "url": "2.0.0a13.post1/advanced/permission.html",
    "revision": "6d94e224614ce7f579159786cc6dd424"
  },
  {
    "url": "2.0.0a13.post1/advanced/publish-plugin.html",
    "revision": "5de18a4414166129006b19687ed42c63"
  },
  {
    "url": "2.0.0a13.post1/advanced/runtime-hook.html",
    "revision": "9353f7dd4840107c2705b045fabea26d"
  },
  {
    "url": "2.0.0a13.post1/advanced/scheduler.html",
    "revision": "6dd7c54c2f6e71038414b54baff824c3"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/cqhttp.html",
    "revision": "f389d6fdb93cb2196ad73bf87f1a5cb1"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/ding.html",
    "revision": "17924ce0ea93019d5d294e729600ec35"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/index.html",
    "revision": "10180ea4fc2806a273addaf2ccd607a6"
  },
  {
    "url": "2.0.0a13.post1/api/adapters/mirai.html",
    "revision": "65017361c766d63233d1dd90dd74b715"
  },
  {
    "url": "2.0.0a13.post1/api/config.html",
    "revision": "faebb8453b5ce695194f640c23a7760e"
  },
  {
    "url": "2.0.0a13.post1/api/drivers/fastapi.html",
    "revision": "a08d0536b5009b95690682b7ddf9679e"
  },
  {
    "url": "2.0.0a13.post1/api/drivers/index.html",
    "revision": "f10f5d331b479561191014c524bd3b68"
  },
  {
    "url": "2.0.0a13.post1/api/drivers/quart.html",
    "revision": "559c4ec012d2bf9a9b73feb55f8077f2"
  },
  {
    "url": "2.0.0a13.post1/api/exception.html",
    "revision": "cec4312a5b25560208895cc22f417ec5"
  },
  {
    "url": "2.0.0a13.post1/api/handler.html",
    "revision": "6ed314406e84ec6404d10506eada92de"
  },
  {
    "url": "2.0.0a13.post1/api/index.html",
    "revision": "72961450b84406b494bac96edb1bf9fc"
  },
  {
    "url": "2.0.0a13.post1/api/log.html",
    "revision": "711ae56f1425b0f979dc229d9c0fefdb"
  },
  {
    "url": "2.0.0a13.post1/api/matcher.html",
    "revision": "d43083c5e74f890443f4213bc1eae56a"
  },
  {
    "url": "2.0.0a13.post1/api/message.html",
    "revision": "7423948775f72a08b2bf04ec1877b83b"
  },
  {
    "url": "2.0.0a13.post1/api/nonebot.html",
    "revision": "83ac95ff9f06742c598e0f00b15e10f3"
  },
  {
    "url": "2.0.0a13.post1/api/permission.html",
    "revision": "44af109ade55351c999f34977c044596"
  },
  {
    "url": "2.0.0a13.post1/api/plugin.html",
    "revision": "be687679af4be213d89cbb9be4307140"
  },
  {
    "url": "2.0.0a13.post1/api/rule.html",
    "revision": "f37868eee9ae9e466edf1445e1eef2ed"
  },
  {
    "url": "2.0.0a13.post1/api/typing.html",
    "revision": "130f6a069d4c0b6c8d9e10700a1e8003"
  },
  {
    "url": "2.0.0a13.post1/api/utils.html",
    "revision": "62efbf3d7f8f8533b955884ca26051d4"
  },
  {
    "url": "2.0.0a13.post1/guide/basic-configuration.html",
    "revision": "b1e8a199eb76e33e3984f3521e7b4002"
  },
  {
    "url": "2.0.0a13.post1/guide/cqhttp-guide.html",
    "revision": "50515b99e2cf3ce134e805dc3485450d"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-handler.html",
    "revision": "17a238c9dd0d12dd6c9a98de16b5facc"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-matcher.html",
    "revision": "2a13eaa97cf5e5aaca8425eb9fb6e9a0"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-plugin.html",
    "revision": "e063f60e263d5ffb59c8514a8aa0f1df"
  },
  {
    "url": "2.0.0a13.post1/guide/creating-a-project.html",
    "revision": "c986396a31c5cb991bc8f7bad676259a"
  },
  {
    "url": "2.0.0a13.post1/guide/ding-guide.html",
    "revision": "252c9c23598dd7d159b1b26ab20a990c"
  },
  {
    "url": "2.0.0a13.post1/guide/end-or-start.html",
    "revision": "1ebdf885bf0f921c95c9ddcfb395419f"
  },
  {
    "url": "2.0.0a13.post1/guide/getting-started.html",
    "revision": "debde81e7a529bc3413a53e3840a9115"
  },
  {
    "url": "2.0.0a13.post1/guide/index.html",
    "revision": "1e651f4939d03653122812b60328eff5"
  },
  {
    "url": "2.0.0a13.post1/guide/installation.html",
    "revision": "1f9e52d608aa9e1f2449165ec5244294"
  },
  {
    "url": "2.0.0a13.post1/guide/loading-a-plugin.html",
    "revision": "c62ceee2627ba91073ff871818293513"
  },
  {
    "url": "2.0.0a13.post1/guide/mirai-guide.html",
    "revision": "eb1fd00bcaac1bffd59bd0aefa927f58"
  },
  {
    "url": "2.0.0a13.post1/index.html",
    "revision": "7aa9b67d6c885ca518c8068327afa07a"
  },
  {
    "url": "2.0.0a7/advanced/export-and-require.html",
    "revision": "32573e7a34e9b3141e4d3cdfb487c832"
  },
  {
    "url": "2.0.0a7/advanced/index.html",
    "revision": "a457c9f91de788cdf2cf4d4b9be5c94b"
  },
  {
    "url": "2.0.0a7/advanced/permission.html",
    "revision": "5f73296d29a8ca31309b6532f9afd9d4"
  },
  {
    "url": "2.0.0a7/advanced/publish-plugin.html",
    "revision": "ad2ceec4a6364bf1f9cb1e03f8f8b32b"
  },
  {
    "url": "2.0.0a7/advanced/runtime-hook.html",
    "revision": "a34a37ff2ba3997680efbe717ea64a19"
  },
  {
    "url": "2.0.0a7/advanced/scheduler.html",
    "revision": "353f591fcd60f6eeda4aa788bad116e0"
  },
  {
    "url": "2.0.0a7/api/adapters/cqhttp.html",
    "revision": "c101aa16f4ee6e47ec0f70d14fc3e2a6"
  },
  {
    "url": "2.0.0a7/api/adapters/ding.html",
    "revision": "b38706e147c4892ee14e7b8cc7f40cec"
  },
  {
    "url": "2.0.0a7/api/adapters/index.html",
    "revision": "041aa473138bcde663474ac411f503b7"
  },
  {
    "url": "2.0.0a7/api/config.html",
    "revision": "eb5db2f9dbe3da0c2da5c9b46f66a8b7"
  },
  {
    "url": "2.0.0a7/api/drivers/fastapi.html",
    "revision": "e123ff442f03e33d05af02166c9e05ae"
  },
  {
    "url": "2.0.0a7/api/drivers/index.html",
    "revision": "49ffb4b6dff1c7f4f8a88a7a5470e59f"
  },
  {
    "url": "2.0.0a7/api/exception.html",
    "revision": "2ab623e4d5597dad75c02775f4a10ab7"
  },
  {
    "url": "2.0.0a7/api/index.html",
    "revision": "4db1f2ff5f3c64cdb9a8ffb908255060"
  },
  {
    "url": "2.0.0a7/api/log.html",
    "revision": "fd977700e54d051c34c5a723385589e8"
  },
  {
    "url": "2.0.0a7/api/matcher.html",
    "revision": "7db3741d57cb1731d1b422b943c6a4f1"
  },
  {
    "url": "2.0.0a7/api/message.html",
    "revision": "57c57d96a86224f23064225c2791b569"
  },
  {
    "url": "2.0.0a7/api/nonebot.html",
    "revision": "bdb6cbcb939208f71e1a8a3de6e0759b"
  },
  {
    "url": "2.0.0a7/api/permission.html",
    "revision": "698b810e15b4445895f4299a2f2e7023"
  },
  {
    "url": "2.0.0a7/api/plugin.html",
    "revision": "5820d44b73cde67c9a0f09aa9e931241"
  },
  {
    "url": "2.0.0a7/api/rule.html",
    "revision": "6ee7c764802ab71b6012bf53dbcf9792"
  },
  {
    "url": "2.0.0a7/api/typing.html",
    "revision": "c4f7266318c729abb6163d940ccb056c"
  },
  {
    "url": "2.0.0a7/api/utils.html",
    "revision": "31eed7145865af765a48e749c5108e29"
  },
  {
    "url": "2.0.0a7/guide/basic-configuration.html",
    "revision": "6fca39be16cbe467c2f4d4d00c97ce29"
  },
  {
    "url": "2.0.0a7/guide/creating-a-handler.html",
    "revision": "21641992fd25c800dc552e60dcd7e995"
  },
  {
    "url": "2.0.0a7/guide/creating-a-matcher.html",
    "revision": "bc1bcdbf0957d236c5b13f9127d1d078"
  },
  {
    "url": "2.0.0a7/guide/creating-a-plugin.html",
    "revision": "0532c3c2fc958c3c37bc5b66f2e19588"
  },
  {
    "url": "2.0.0a7/guide/creating-a-project.html",
    "revision": "87d1a212bfad4d2822512e875bc85cc5"
  },
  {
    "url": "2.0.0a7/guide/end-or-start.html",
    "revision": "9df933f14c5ea0718bf6522508cdccba"
  },
  {
    "url": "2.0.0a7/guide/getting-started.html",
    "revision": "812e12acd923ca4e6463379c880630e6"
  },
  {
    "url": "2.0.0a7/guide/index.html",
    "revision": "f83ecc870e9e600776bc5297685131ec"
  },
  {
    "url": "2.0.0a7/guide/installation.html",
    "revision": "179bdd372306598f6e6f08a6f984a030"
  },
  {
    "url": "2.0.0a7/guide/loading-a-plugin.html",
    "revision": "9cb7c78e3f88c04241fd20b3bd73c7b1"
  },
  {
    "url": "2.0.0a7/index.html",
    "revision": "d5e3536d5a5ad8092ece7ab09bc3eadd"
  },
  {
    "url": "2.0.0a8.post2/advanced/export-and-require.html",
    "revision": "4a3fd376418c5e84f1ec31d9064cfd80"
  },
  {
    "url": "2.0.0a8.post2/advanced/index.html",
    "revision": "14f3962d6ffac246c8a93c21463152f5"
  },
  {
    "url": "2.0.0a8.post2/advanced/overloaded-handlers.html",
    "revision": "1a4167ead0c7e57c1df6e805f6ba4288"
  },
  {
    "url": "2.0.0a8.post2/advanced/permission.html",
    "revision": "3c2ac92eebbba05929c7e280473b5201"
  },
  {
    "url": "2.0.0a8.post2/advanced/publish-plugin.html",
    "revision": "570f46d8c13cb6182f10e330521cf5e6"
  },
  {
    "url": "2.0.0a8.post2/advanced/runtime-hook.html",
    "revision": "cc6266b7448908b829c13fe9f5ad6241"
  },
  {
    "url": "2.0.0a8.post2/advanced/scheduler.html",
    "revision": "e693a6f9770ca3066349c1ad144f3566"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/cqhttp.html",
    "revision": "50c5cc3215233318b65e5ef28cf94ac6"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/ding.html",
    "revision": "7c27e80aee3908c67db124cf5754ce99"
  },
  {
    "url": "2.0.0a8.post2/api/adapters/index.html",
    "revision": "a96044e470ba8ddd8fb49523aa4e03a7"
  },
  {
    "url": "2.0.0a8.post2/api/config.html",
    "revision": "c74bf2b99c6ddfe501c6fbc9bd706014"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/fastapi.html",
    "revision": "86e22a65d815787b1f57f8a1d096f50f"
  },
  {
    "url": "2.0.0a8.post2/api/drivers/index.html",
    "revision": "a0d2474fca9aa82de27262aa20db3c51"
  },
  {
    "url": "2.0.0a8.post2/api/exception.html",
    "revision": "22bfa74b80070efe68ba05550ac288f4"
  },
  {
    "url": "2.0.0a8.post2/api/index.html",
    "revision": "bc5656743539caeacae97b381d317c9b"
  },
  {
    "url": "2.0.0a8.post2/api/log.html",
    "revision": "b13087c00cd2342088a103ef253bc5f5"
  },
  {
    "url": "2.0.0a8.post2/api/matcher.html",
    "revision": "d020d8184cc4086e49d60e4749d82cce"
  },
  {
    "url": "2.0.0a8.post2/api/message.html",
    "revision": "71c7618c969b358a46c1eb7b9df065c7"
  },
  {
    "url": "2.0.0a8.post2/api/nonebot.html",
    "revision": "a71dd59d9b712d53c25120cfc9c8cc6c"
  },
  {
    "url": "2.0.0a8.post2/api/permission.html",
    "revision": "c29f1815f9ea7433b77177066e380ee9"
  },
  {
    "url": "2.0.0a8.post2/api/plugin.html",
    "revision": "30681ae27675fd7428ccca10d303e8b5"
  },
  {
    "url": "2.0.0a8.post2/api/rule.html",
    "revision": "7be3824df488aa4cf5daecba79a4e908"
  },
  {
    "url": "2.0.0a8.post2/api/typing.html",
    "revision": "3d9519a31c172577a291f1cbac47c378"
  },
  {
    "url": "2.0.0a8.post2/api/utils.html",
    "revision": "3fef1ed8e35510d3db287dd1f230861f"
  },
  {
    "url": "2.0.0a8.post2/guide/basic-configuration.html",
    "revision": "b9a253b6e742a65d317a53ad99b06f22"
  },
  {
    "url": "2.0.0a8.post2/guide/cqhttp-guide.html",
    "revision": "c7bae40c048c171b160cd22e47a0640d"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-handler.html",
    "revision": "0e2aea17acba7fbbd5b341778e3dde7e"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-matcher.html",
    "revision": "921575275d0ba94297a390f758f8515b"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-plugin.html",
    "revision": "99aee0c0f1c2e76a030c1122f9c60f9c"
  },
  {
    "url": "2.0.0a8.post2/guide/creating-a-project.html",
    "revision": "e057e7020444de2fad1af947403dbbff"
  },
  {
    "url": "2.0.0a8.post2/guide/ding-guide.html",
    "revision": "00819c75258eece2063c39ad3a087d4b"
  },
  {
    "url": "2.0.0a8.post2/guide/end-or-start.html",
    "revision": "2b9320df75c61661321a9ca2a851a5a0"
  },
  {
    "url": "2.0.0a8.post2/guide/getting-started.html",
    "revision": "3e840f1d80812ef80ce75c96f6707e37"
  },
  {
    "url": "2.0.0a8.post2/guide/index.html",
    "revision": "d757638960a08c244063b337a689097c"
  },
  {
    "url": "2.0.0a8.post2/guide/installation.html",
    "revision": "3b9eb1c7e4b248152ed2a8e526b70f8c"
  },
  {
    "url": "2.0.0a8.post2/guide/loading-a-plugin.html",
    "revision": "87da44c31b3a3b386784ff8002554628"
  },
  {
    "url": "2.0.0a8.post2/index.html",
    "revision": "3e07eeac9078b8ed4a6412c6c535d30d"
  },
  {
    "url": "404.html",
    "revision": "07822e7a656f711e568aa0fba03f66e8"
  },
  {
    "url": "advanced/export-and-require.html",
    "revision": "8cc837b4861f8c15b979f0321dfff255"
  },
  {
    "url": "advanced/index.html",
    "revision": "c3fdfe4936a3c56b93aea2b78db1b2d2"
  },
  {
    "url": "advanced/overloaded-handlers.html",
    "revision": "8cce962bf7751e600a0ff044a0023fa8"
  },
  {
    "url": "advanced/permission.html",
    "revision": "7719bd1031bbe6b64c987dfa6a52f010"
  },
  {
    "url": "advanced/publish-plugin.html",
    "revision": "0b442b440b5521bf2b9b58310dcc758d"
  },
  {
    "url": "advanced/runtime-hook.html",
    "revision": "87989a951706524b5a64caf50a4748c4"
  },
  {
    "url": "advanced/scheduler.html",
    "revision": "65d25eec3e399210f4bb7ea4d6ef554f"
  },
  {
    "url": "api/adapters/cqhttp.html",
    "revision": "2ded1a6a9fa7d9e7a21524caf9b86cea"
  },
  {
    "url": "api/adapters/ding.html",
    "revision": "106fdc80debc6a3088881106138195e3"
  },
  {
    "url": "api/adapters/feishu.html",
    "revision": "e4dec84120e982aff33c33f391690a42"
  },
  {
    "url": "api/adapters/index.html",
    "revision": "b6a720c8136a58fc623ef00fdf883a73"
  },
  {
    "url": "api/adapters/mirai.html",
    "revision": "b0a081f3ee80ef7fd54b604a79d52559"
  },
  {
    "url": "api/config.html",
    "revision": "4fa8b794a199d40ec427514211bd4c0b"
  },
  {
    "url": "api/drivers/aiohttp.html",
    "revision": "b565c5f562b428caf4b2fac298d849e8"
  },
  {
    "url": "api/drivers/fastapi.html",
    "revision": "7a71685316f6d83ebd6bd47c16443d91"
  },
  {
    "url": "api/drivers/index.html",
    "revision": "0ff1bd01e76808007b14853c238f475b"
  },
  {
    "url": "api/drivers/quart.html",
    "revision": "af8d636386886276c30565dfaf55dce0"
  },
  {
    "url": "api/exception.html",
    "revision": "85577bf3fccf797af82a02d0f1bc5533"
  },
  {
    "url": "api/handler.html",
    "revision": "d88ed84a9e1f0a26c752dbde13b2febf"
  },
  {
    "url": "api/index.html",
    "revision": "29cf751545b1752117f15f42b0120be0"
  },
  {
    "url": "api/log.html",
    "revision": "9cee9ebe2f04f95d3ad997ffb91a0ac7"
  },
  {
    "url": "api/matcher.html",
    "revision": "b237cf031727a4f11a3779ea811a19d3"
  },
  {
    "url": "api/message.html",
    "revision": "a844c441792e670829028c9d3f4ec52f"
  },
  {
    "url": "api/nonebot.html",
    "revision": "6aa783ad07f109b59789f8d6ff754a71"
  },
  {
    "url": "api/permission.html",
    "revision": "331bb232cdb8589bae830a3747dfb6fb"
  },
  {
    "url": "api/plugin.html",
    "revision": "c9ac0a7b9b669e0edc7ff8aa53b4c8f0"
  },
  {
    "url": "api/rule.html",
    "revision": "336e5835dc78d9b0577426a705d5b799"
  },
  {
    "url": "api/typing.html",
    "revision": "0ca079e3ac96a3f9a500ec97bbd60f89"
  },
  {
    "url": "api/utils.html",
    "revision": "0996b4e7fe59b92390f72c022e9b368d"
  },
  {
    "url": "assets/css/0.styles.92d96405.css",
    "revision": "5a3d1d298d6ccc32ea2699b83042f28b"
  },
  {
    "url": "assets/img/Handle-Event.1e964e39.png",
    "revision": "1e964e39a1e302bc36072da2ffe9f509"
  },
  {
    "url": "assets/img/jiaqian.9b09040e.png",
    "revision": "9b09040ed4e5e35000247aa00e6dceac"
  },
  {
    "url": "assets/img/search.237d6f6a.svg",
    "revision": "237d6f6a3fe211d00a61e871a263e9fe"
  },
  {
    "url": "assets/img/search.83621669.svg",
    "revision": "83621669651b9a3d4bf64d1a670ad856"
  },
  {
    "url": "assets/img/webhook.479198ed.png",
    "revision": "479198ed677c8ba4bbdf72d0a60497c9"
  },
  {
    "url": "assets/js/10.3eef6e40.js",
    "revision": "657f042b2f13f05b7b1fde501cdc6d19"
  },
  {
    "url": "assets/js/100.b90f771b.js",
    "revision": "5734bcb39a3ab218d1a1cd0dfea2080a"
  },
  {
    "url": "assets/js/101.9fedf102.js",
    "revision": "f8d71cbb2284ba7e81142dce84cb6eee"
  },
  {
    "url": "assets/js/102.27c2a45e.js",
    "revision": "e90ce5b9904ce08ebda166f71a656cc1"
  },
  {
    "url": "assets/js/103.8eb9ee84.js",
    "revision": "0684551703a5794be1677aeb313b751e"
  },
  {
    "url": "assets/js/104.e424f4ff.js",
    "revision": "a1b1cf3544abc3f44e393d4811d1bfd9"
  },
  {
    "url": "assets/js/105.862e96f7.js",
    "revision": "ac7d3034aedc479bde1871755fdd2b7c"
  },
  {
    "url": "assets/js/106.7a5f497b.js",
    "revision": "39bad748ba86322a0bf7d0f53d735cd7"
  },
  {
    "url": "assets/js/107.299122a8.js",
    "revision": "13aba9db9d9d60efa355f9e31c5a0bdb"
  },
  {
    "url": "assets/js/108.088c2754.js",
    "revision": "e08d372118f29d5a166eb2bddd762413"
  },
  {
    "url": "assets/js/109.1a315a1d.js",
    "revision": "5257dee72d93b5308bcbbfd14f7ac6f3"
  },
  {
    "url": "assets/js/11.d3a7a219.js",
    "revision": "bb599edf2ec9202ca89d8c052e98f878"
  },
  {
    "url": "assets/js/110.e8a7245b.js",
    "revision": "6700b71e555b10709c5f524960beaf01"
  },
  {
    "url": "assets/js/111.68ea9474.js",
    "revision": "962d12d754c1f9d7a3cee105772419c0"
  },
  {
    "url": "assets/js/112.125b3e19.js",
    "revision": "b9c259ef441194ca7363d62d7118e604"
  },
  {
    "url": "assets/js/113.0d92a3d0.js",
    "revision": "bd7d48bb305afc16e1d12a0a35cb469f"
  },
  {
    "url": "assets/js/114.0f2a780d.js",
    "revision": "e08a06769951609ba79401c73e0d955c"
  },
  {
    "url": "assets/js/115.dc0d9b8b.js",
    "revision": "263f4d36f98a499ed3cc4c05e0786196"
  },
  {
    "url": "assets/js/116.57a15bf4.js",
    "revision": "34111df6c41f5c376d7e6c46c73ac826"
  },
  {
    "url": "assets/js/117.d68a383e.js",
    "revision": "76c1451e112e41887a967b973be76d2f"
  },
  {
    "url": "assets/js/118.cc20a445.js",
    "revision": "d425c6e7b2190e9fbd2fb547bc3ccb81"
  },
  {
    "url": "assets/js/119.101378d4.js",
    "revision": "3c4d080973d971b8155de339a1049f17"
  },
  {
    "url": "assets/js/12.81060290.js",
    "revision": "8f4ea0ddfe721fdcf26af94fab877ad9"
  },
  {
    "url": "assets/js/120.ef4b7aed.js",
    "revision": "69b9a725ccb4ec63fab7b6880ba942c5"
  },
  {
    "url": "assets/js/121.5a3da29e.js",
    "revision": "9efe06db8a3e3aa4e93ebac75614b2be"
  },
  {
    "url": "assets/js/122.a8ffd757.js",
    "revision": "7a358687bae23d05c78025d3d6a6176b"
  },
  {
    "url": "assets/js/123.cec76181.js",
    "revision": "f64d1879812ca3e1af4627bfdb716536"
  },
  {
    "url": "assets/js/124.fc5e0d38.js",
    "revision": "04a0554ab3fbeac294f99a0b997360ab"
  },
  {
    "url": "assets/js/125.83acc842.js",
    "revision": "7f37528abaf5dcc7e0fbc9cba3f58895"
  },
  {
    "url": "assets/js/126.5b644d5d.js",
    "revision": "1c42a377c9ce36dcc643c1c346d876cc"
  },
  {
    "url": "assets/js/127.b4f32d0b.js",
    "revision": "3546c6c8608b7fc7b12f6a994b219c4b"
  },
  {
    "url": "assets/js/128.b6b76273.js",
    "revision": "85579613eaec09dd045b891b94d7606d"
  },
  {
    "url": "assets/js/129.033f1cf8.js",
    "revision": "6db545590a92a3f400ed9cd76387e2cc"
  },
  {
    "url": "assets/js/13.36401754.js",
    "revision": "7bdc5c33c45c0d1263a2a14c50a118b4"
  },
  {
    "url": "assets/js/130.d88e1f4b.js",
    "revision": "6ab73a4f3513b8b87bb0afecb9c92a68"
  },
  {
    "url": "assets/js/131.33fe54cc.js",
    "revision": "6901ccead2b52724a14c61213956cdbf"
  },
  {
    "url": "assets/js/132.88bace4d.js",
    "revision": "13791760d5ba947014b9c3c670ffb14f"
  },
  {
    "url": "assets/js/133.fa51eaa2.js",
    "revision": "0b033d272264b935321d88eec7710fee"
  },
  {
    "url": "assets/js/134.de424697.js",
    "revision": "acfe0d7ada631101996dd26f7ac7162a"
  },
  {
    "url": "assets/js/135.e4a78624.js",
    "revision": "5c9fec8e5dce50816ab17d5b9a9b815b"
  },
  {
    "url": "assets/js/136.c543a118.js",
    "revision": "3f95b12418b6e41e27776466d0ecf37a"
  },
  {
    "url": "assets/js/137.c007e4df.js",
    "revision": "d87983e76ec25049636422719e14eb5e"
  },
  {
    "url": "assets/js/138.5a3a5e72.js",
    "revision": "30af8820b427437ad7290a8de8ea1c40"
  },
  {
    "url": "assets/js/139.cee2fad2.js",
    "revision": "28d00face1b910fa9610cad6f53b8b15"
  },
  {
    "url": "assets/js/14.e1dc0be5.js",
    "revision": "21632c5f9dd9045995120f9aee94509c"
  },
  {
    "url": "assets/js/140.62ef1d0e.js",
    "revision": "edd6922ce48ff369c6d93612a6ff3a8c"
  },
  {
    "url": "assets/js/141.c797adcf.js",
    "revision": "d59bf664c53428b94b7f26ea36d0e2b8"
  },
  {
    "url": "assets/js/142.5d1f3e06.js",
    "revision": "f63d6ad5c31103f13c9beec6c0cf8791"
  },
  {
    "url": "assets/js/143.1ff35cca.js",
    "revision": "200515b65e58eb23ef52eeb10770dcdc"
  },
  {
    "url": "assets/js/144.972bdca1.js",
    "revision": "e9127b964714dbfb7ab2637397e0cab9"
  },
  {
    "url": "assets/js/145.1cd179bb.js",
    "revision": "cd6c353b215e48d2f43d0a3d9428f47b"
  },
  {
    "url": "assets/js/146.9fbdd928.js",
    "revision": "2666d378951969f7d35da54b7fa96445"
  },
  {
    "url": "assets/js/147.f9b0cca8.js",
    "revision": "e521810195a85835575659b3f1632a0b"
  },
  {
    "url": "assets/js/148.22528477.js",
    "revision": "36f4e6993ff956b95b80204aa168b2fc"
  },
  {
    "url": "assets/js/149.6939e2e9.js",
    "revision": "d8ccb150337b4a401b786cdb6b32b2f9"
  },
  {
    "url": "assets/js/15.5009a47a.js",
    "revision": "3ffc659eff67c15017196f421a4a7b09"
  },
  {
    "url": "assets/js/150.67520d0e.js",
    "revision": "ffa41bb8f3cc3b49dfa39eca09e45aa5"
  },
  {
    "url": "assets/js/151.e6a59faf.js",
    "revision": "87dbaa83ba235461a97edd674491a19a"
  },
  {
    "url": "assets/js/152.6553619a.js",
    "revision": "8757439b6577912de7cceaa54d0a4edb"
  },
  {
    "url": "assets/js/153.c2ad7863.js",
    "revision": "00bfaf71bac256241e3a63b6d4c5c2ec"
  },
  {
    "url": "assets/js/154.ad50a312.js",
    "revision": "d9ea6bd818b4b3909f8b4a95e1cb88fa"
  },
  {
    "url": "assets/js/155.328903d3.js",
    "revision": "ecbdc1991b6313d5c9c9d24e0dffa005"
  },
  {
    "url": "assets/js/156.183446c8.js",
    "revision": "be9e6c21a9449cb49bcfc251e5cf5363"
  },
  {
    "url": "assets/js/157.3b4cda49.js",
    "revision": "5ab1c233d3fe601303ccc355c3136ae2"
  },
  {
    "url": "assets/js/158.b5bbdc0e.js",
    "revision": "e6ebfed15fece2be9a491c301e908b33"
  },
  {
    "url": "assets/js/159.f7d39921.js",
    "revision": "4f6ef1e701e0974e4caad1d6cb532ea8"
  },
  {
    "url": "assets/js/16.26678ae8.js",
    "revision": "10afa817d027980e747594efdf936842"
  },
  {
    "url": "assets/js/160.2cd9ade1.js",
    "revision": "72150f20b1eaa6f919ca182b65c5aafc"
  },
  {
    "url": "assets/js/161.9cbeac08.js",
    "revision": "72eeff276b65f120ead6f5e6abdef1d0"
  },
  {
    "url": "assets/js/162.fb37a531.js",
    "revision": "735e8b12bbb60bdb2d3147b6dd2b575a"
  },
  {
    "url": "assets/js/163.443226af.js",
    "revision": "dc05c049a306a155a2a1a635fd7632f3"
  },
  {
    "url": "assets/js/164.c589e0fe.js",
    "revision": "5ce55abfc2fadd50d428cf5e8797c6df"
  },
  {
    "url": "assets/js/165.9572c3e9.js",
    "revision": "c5a0fa37c7d120fbd20c21efb7057bd8"
  },
  {
    "url": "assets/js/166.fa839f30.js",
    "revision": "ae8065861f8c779a297d6d89947d04f9"
  },
  {
    "url": "assets/js/167.7c3a88cf.js",
    "revision": "34d70af0a05dcabdb99570be57196a20"
  },
  {
    "url": "assets/js/168.68d5bfc6.js",
    "revision": "0ee9970638881141d7b598ebdf260095"
  },
  {
    "url": "assets/js/169.a579c78a.js",
    "revision": "b38910106db3609be4b8ff9e6df812b5"
  },
  {
    "url": "assets/js/17.763ec2e8.js",
    "revision": "b4f6f8a557c2becd7793f9952b43e0d5"
  },
  {
    "url": "assets/js/170.c8b15be9.js",
    "revision": "efd59f223e9f9bfce17cad271df30759"
  },
  {
    "url": "assets/js/171.a2d06493.js",
    "revision": "109bcc5e00a5905b2d0f4d2fd40faf3a"
  },
  {
    "url": "assets/js/172.acba45d0.js",
    "revision": "5c8372d1d507bc60c4a2c146f23dbeb2"
  },
  {
    "url": "assets/js/173.1081032c.js",
    "revision": "561b4db26b30444ce3d2b9d66c9b84b4"
  },
  {
    "url": "assets/js/174.4e0de1ca.js",
    "revision": "9ed5090aaac19c4064356d7833b26645"
  },
  {
    "url": "assets/js/175.a30c4351.js",
    "revision": "6cbc4d04d5e3e5a89215043759a221e3"
  },
  {
    "url": "assets/js/176.1403f2eb.js",
    "revision": "40f0afdc249ed28260d035ba5b45c015"
  },
  {
    "url": "assets/js/177.3fde5517.js",
    "revision": "4ba447c067c03e691f24180c1d872e6c"
  },
  {
    "url": "assets/js/178.b57f9665.js",
    "revision": "85025779f116a449393085b7b19f1a25"
  },
  {
    "url": "assets/js/179.187bec29.js",
    "revision": "cb3e1616bfb2cb627e0df53cf6532cc8"
  },
  {
    "url": "assets/js/18.3964d78a.js",
    "revision": "97d9914df5e1b17418dff146a7afc34f"
  },
  {
    "url": "assets/js/180.90025091.js",
    "revision": "b88ad9995b2b96a555f5c520dca97792"
  },
  {
    "url": "assets/js/181.72fc6300.js",
    "revision": "260b6484ba85aa59ea42cefab2cc396e"
  },
  {
    "url": "assets/js/182.06a7c6da.js",
    "revision": "22cdd0e3fec98a669f4a5a23a84f597d"
  },
  {
    "url": "assets/js/183.ecef2df6.js",
    "revision": "d1a9e0b9c5cfc3cf1f1ffc71b602d702"
  },
  {
    "url": "assets/js/184.840732d4.js",
    "revision": "19f4166430f959859d03941ed08666c0"
  },
  {
    "url": "assets/js/185.9fd07a30.js",
    "revision": "a9ff19fe4a412ac9873fce016c704289"
  },
  {
    "url": "assets/js/186.ddee830a.js",
    "revision": "1707df5efddafaee422df5128e9f50c8"
  },
  {
    "url": "assets/js/187.1bbff6f5.js",
    "revision": "9e16b6e331d0b952113ed3d35e272aef"
  },
  {
    "url": "assets/js/188.a5ea22ae.js",
    "revision": "7a6d88bd03dd35cdd6f8acbc863b40a8"
  },
  {
    "url": "assets/js/189.958bec88.js",
    "revision": "f552a4240fd82572f71471d340545500"
  },
  {
    "url": "assets/js/19.73881999.js",
    "revision": "344c83e1a1cbe28661de7493154b51a5"
  },
  {
    "url": "assets/js/190.c28d4588.js",
    "revision": "1a858cc99c9d86f9236d6658b87bc36d"
  },
  {
    "url": "assets/js/191.f7939d07.js",
    "revision": "be48d4bb2659f7742b42f137dbf1b4c6"
  },
  {
    "url": "assets/js/192.a7fcfbf6.js",
    "revision": "468b5ea38a431f03050b776e79224df1"
  },
  {
    "url": "assets/js/193.f286bcf7.js",
    "revision": "ae32d1b5f612c084debfdd66d846b5b3"
  },
  {
    "url": "assets/js/194.b87e3ada.js",
    "revision": "95571a37057b5b9fa6fac3cf8d6be15a"
  },
  {
    "url": "assets/js/195.1fd4cc16.js",
    "revision": "994317cb0cc763a3f86307dcee59f976"
  },
  {
    "url": "assets/js/196.fdc28896.js",
    "revision": "cfae8e7ba0fbff063dd2ee5834f85bae"
  },
  {
    "url": "assets/js/197.b63025ef.js",
    "revision": "2c1d546d7cb92fda74d4fbfb333ff324"
  },
  {
    "url": "assets/js/198.f3fd748f.js",
    "revision": "0cbf8aff3310bd197f2a71159831a82d"
  },
  {
    "url": "assets/js/199.fce42211.js",
    "revision": "3742e9cce31baac1cb69a792a0b30113"
  },
  {
    "url": "assets/js/20.93ddafaf.js",
    "revision": "b910f43c26a8d69ac5e46337ac92a869"
  },
  {
    "url": "assets/js/200.d2d832ee.js",
    "revision": "20454d152ca9964fecb153149c9acd1e"
  },
  {
    "url": "assets/js/201.f49a50d8.js",
    "revision": "9f47cd01a2c668269c03bf71e4145280"
  },
  {
    "url": "assets/js/202.30b71f79.js",
    "revision": "48f799e21151643f287b3e84dd6e701b"
  },
  {
    "url": "assets/js/203.f6ad6a83.js",
    "revision": "cac9128e083976703afda51b5dc4437e"
  },
  {
    "url": "assets/js/204.0c3a9899.js",
    "revision": "5ad1110dd0b840506b9da3dfee6ef65f"
  },
  {
    "url": "assets/js/205.b37f719b.js",
    "revision": "2bd5b497108410f8bd8fa2e453b1b1bb"
  },
  {
    "url": "assets/js/206.f421ce3d.js",
    "revision": "6c9fefaeb0fd9d4f42b87367006d6b55"
  },
  {
    "url": "assets/js/207.547f4269.js",
    "revision": "3edeff146035872f96f280f9a87a4cdc"
  },
  {
    "url": "assets/js/208.b5d501bb.js",
    "revision": "a8fa2540c49b8ce59b622653052d71b4"
  },
  {
    "url": "assets/js/209.d9853e32.js",
    "revision": "e308fac4f3430269ea79a0403c12baf8"
  },
  {
    "url": "assets/js/21.c5df92ca.js",
    "revision": "f98e94211e70fe1d14d594a27469c08f"
  },
  {
    "url": "assets/js/210.00c61260.js",
    "revision": "7a0bf700e6c3ac7623d32a1159a6b884"
  },
  {
    "url": "assets/js/211.4e111060.js",
    "revision": "fc1a9959eb2550f90d0c1b39368072b8"
  },
  {
    "url": "assets/js/212.5d02684a.js",
    "revision": "114ab005960b63d0937125442102947d"
  },
  {
    "url": "assets/js/213.dd870a1f.js",
    "revision": "f0b0e11bbf7281e1ad1d122bc28a9812"
  },
  {
    "url": "assets/js/214.50423149.js",
    "revision": "024289015d3688c17b0f336689074d7f"
  },
  {
    "url": "assets/js/215.9f662bfe.js",
    "revision": "3b2fc024944a597936c3fbc3b7150b2a"
  },
  {
    "url": "assets/js/216.40fbcd84.js",
    "revision": "7b437ea9c5e04f75751bc938b7804d0f"
  },
  {
    "url": "assets/js/217.693c7894.js",
    "revision": "66eb73b3a462508e733b056fbd79a544"
  },
  {
    "url": "assets/js/218.d0e705d4.js",
    "revision": "bcd47ff25b5481ddd21d0d588cd4460c"
  },
  {
    "url": "assets/js/219.ba207ae7.js",
    "revision": "fa3d51316e9f8620c2109ead1496f353"
  },
  {
    "url": "assets/js/22.6a304c43.js",
    "revision": "7e3726c44ae88d354b3fd3fe677a863f"
  },
  {
    "url": "assets/js/220.513da117.js",
    "revision": "cc83c189aa7e61caa698d76de9c6ea3f"
  },
  {
    "url": "assets/js/221.4c74258f.js",
    "revision": "ece9556cb47dd6ef9b5bdd8ba6e10e34"
  },
  {
    "url": "assets/js/222.a17cde12.js",
    "revision": "40fc1b052d9e59ca055bf72575864cb3"
  },
  {
    "url": "assets/js/223.563dca32.js",
    "revision": "1c6c2bc1c2f8ae315bf9ed9c69746352"
  },
  {
    "url": "assets/js/224.7fe23144.js",
    "revision": "e7fd30d79253637850226edf075af053"
  },
  {
    "url": "assets/js/225.87cdd17d.js",
    "revision": "6de3cf4a40944753e250fa0cf732a57e"
  },
  {
    "url": "assets/js/226.65c400e2.js",
    "revision": "8be3cabfc90b94942d64659bdeec5301"
  },
  {
    "url": "assets/js/227.afb24d8f.js",
    "revision": "461e8d20cee00d8d15eb2aec0b19b3a6"
  },
  {
    "url": "assets/js/228.dd51e139.js",
    "revision": "d5727068bb854ddba067106a160e5591"
  },
  {
    "url": "assets/js/229.1ef5e97a.js",
    "revision": "5dbe37412391e3878bb2bff91b28463a"
  },
  {
    "url": "assets/js/23.5f807091.js",
    "revision": "db49f5a6d11822d4ae1e548c78a6ff12"
  },
  {
    "url": "assets/js/230.d404fb02.js",
    "revision": "6e3703d62bc9608e643eafdbdc5c921a"
  },
  {
    "url": "assets/js/231.61c16566.js",
    "revision": "e7de7cfaa09e66c8fb37bd8795ecdb1f"
  },
  {
    "url": "assets/js/232.a8582e6c.js",
    "revision": "1e494238a6dfd6e4dc508cfabb551a76"
  },
  {
    "url": "assets/js/233.4846415e.js",
    "revision": "3577a4917e6e09ca99a638b654f9ed9e"
  },
  {
    "url": "assets/js/234.bd7add8e.js",
    "revision": "8d597d697bc30ba142e8d8e028d277c1"
  },
  {
    "url": "assets/js/235.4a3032e6.js",
    "revision": "23a50c787255a61689bd0476de981d36"
  },
  {
    "url": "assets/js/236.2f94cc7a.js",
    "revision": "b379a704a5062ca7b7a10b083c9b69c9"
  },
  {
    "url": "assets/js/237.40c15229.js",
    "revision": "46a18eba90935f7c184f39f5108fe5c1"
  },
  {
    "url": "assets/js/238.4fbb0c66.js",
    "revision": "e81e16730544fdbebdb6f97dd8195674"
  },
  {
    "url": "assets/js/239.f3d235d2.js",
    "revision": "2679479f9bbde32ebf54cc713df52a42"
  },
  {
    "url": "assets/js/24.5a089fe4.js",
    "revision": "47b684d9fff2db494f05cd5d5199be59"
  },
  {
    "url": "assets/js/240.1889a720.js",
    "revision": "81e3caf221297b4cd1867876ce841f26"
  },
  {
    "url": "assets/js/241.92d922d8.js",
    "revision": "ebfe4691d8af7843aa421f0231c17744"
  },
  {
    "url": "assets/js/242.b4fad1da.js",
    "revision": "9a7e1d8b746f3ccfb7fb6665610ae978"
  },
  {
    "url": "assets/js/243.8a9cf0a8.js",
    "revision": "c2303b57b3fad19ebf155052154b7c5e"
  },
  {
    "url": "assets/js/244.a50ce4d9.js",
    "revision": "b0c6cbe2269d1eaa8153332c82bc33e4"
  },
  {
    "url": "assets/js/245.cfa2567b.js",
    "revision": "86a29f12d2e7996eea3aa7d99cd40040"
  },
  {
    "url": "assets/js/246.2578510b.js",
    "revision": "e7abd975da3cf90c7865caeb5b6b6423"
  },
  {
    "url": "assets/js/247.c6a2941c.js",
    "revision": "6b925f7ce5d1e47ee9bf74cb009aa205"
  },
  {
    "url": "assets/js/248.012e8dc1.js",
    "revision": "af32fea3adfa065bebd517f019357a8a"
  },
  {
    "url": "assets/js/249.7e57ccf2.js",
    "revision": "f468c917c4f0a0fe4de700e3a7871575"
  },
  {
    "url": "assets/js/25.692f4d49.js",
    "revision": "08c6c5f59113b8e796af3b0321ebb8c7"
  },
  {
    "url": "assets/js/250.dd5dcfc2.js",
    "revision": "a8f7a6f9b2a4d63408693d15faf21ad0"
  },
  {
    "url": "assets/js/251.58373875.js",
    "revision": "e6c87d7041e1e57a0eb96110ae5c9a36"
  },
  {
    "url": "assets/js/252.41598a00.js",
    "revision": "cfd00919cb45402c3cae763866cfa128"
  },
  {
    "url": "assets/js/253.05118cef.js",
    "revision": "eb815624dfb6e7f72027282c4e9f7442"
  },
  {
    "url": "assets/js/254.a0970771.js",
    "revision": "944c6fdc81e41c2829d17344dd600216"
  },
  {
    "url": "assets/js/255.20a4b6ae.js",
    "revision": "5f5fe7f65850f1ee13475627a4593df1"
  },
  {
    "url": "assets/js/256.df4aafd1.js",
    "revision": "514c03060a36e72c5021637657ed7088"
  },
  {
    "url": "assets/js/26.e9eee22c.js",
    "revision": "cf46e24104851aa15580df55e1c8cd97"
  },
  {
    "url": "assets/js/27.4e0cf912.js",
    "revision": "1e8c71dda6aff0281f6c954b436d4f76"
  },
  {
    "url": "assets/js/28.2ded3eaa.js",
    "revision": "edc5543d3492ac54baa66d0e34e48960"
  },
  {
    "url": "assets/js/29.3e2368e5.js",
    "revision": "aece5ee812956b1936a183c3c2b07f4e"
  },
  {
    "url": "assets/js/3.2e7943ab.js",
    "revision": "bd8658ad1c0c2ed93346ccd97441eafe"
  },
  {
    "url": "assets/js/30.4bbc5af3.js",
    "revision": "505d99b035af971689860d430d17e04a"
  },
  {
    "url": "assets/js/31.99933d71.js",
    "revision": "3eab4819bc3e410c07e15e404fcc8c74"
  },
  {
    "url": "assets/js/32.c1d89a57.js",
    "revision": "aeb58bb6d79e062540edf63a64a2a116"
  },
  {
    "url": "assets/js/33.39c86a9b.js",
    "revision": "5bfce0d80790762542acab60ef2fc949"
  },
  {
    "url": "assets/js/34.254f7d6f.js",
    "revision": "858876a1ba28efd340caa4103853f955"
  },
  {
    "url": "assets/js/35.4918eea5.js",
    "revision": "2917974111d569409cbc0f697b2023ae"
  },
  {
    "url": "assets/js/36.97e6b083.js",
    "revision": "27ba4c61b30c641c45b52597bc89b9dd"
  },
  {
    "url": "assets/js/37.cd6f06f3.js",
    "revision": "d78d8e5cc091e9e333547cfa0cf1072a"
  },
  {
    "url": "assets/js/38.a4f1f250.js",
    "revision": "ac0dd9824a3f3394ee6c00be76c530dd"
  },
  {
    "url": "assets/js/39.4d35e0bd.js",
    "revision": "02bc733fdd228134fd5d1687af7abae2"
  },
  {
    "url": "assets/js/4.38a5a745.js",
    "revision": "e54910fcd7d2ccea0ecc1b0c8d759e32"
  },
  {
    "url": "assets/js/40.43e6d215.js",
    "revision": "dc356888371469a6d001271921697681"
  },
  {
    "url": "assets/js/41.e40dbe00.js",
    "revision": "044ab4a381cf58f874b1913b5c626870"
  },
  {
    "url": "assets/js/42.df765cb2.js",
    "revision": "6208ea4b2a021314d9b4244df916c2f6"
  },
  {
    "url": "assets/js/43.8975fa0a.js",
    "revision": "94070a38dc14b18ac3c3d37999c70847"
  },
  {
    "url": "assets/js/44.0eaf013d.js",
    "revision": "7c6cb60234f79d25352216cfec4fd1f7"
  },
  {
    "url": "assets/js/45.58bb5f6d.js",
    "revision": "b04115a08afd66fd83ca80d2e8faa00b"
  },
  {
    "url": "assets/js/46.1ef18f90.js",
    "revision": "842a1e74c046474d13183987980c8ef6"
  },
  {
    "url": "assets/js/47.0a3f45e6.js",
    "revision": "f1e8535cf36260f6f3a8598e197d2ee9"
  },
  {
    "url": "assets/js/48.b160b436.js",
    "revision": "e6a34540a8d76dc5fb58dcfb5df48978"
  },
  {
    "url": "assets/js/49.77147adc.js",
    "revision": "2c187cc62b748ac722161a3471022106"
  },
  {
    "url": "assets/js/5.f42cec79.js",
    "revision": "cf7bdef3b2137067a0c5573d8097fd63"
  },
  {
    "url": "assets/js/50.6820eb1d.js",
    "revision": "338a6e062fc96129be6d9e4d13c6ab06"
  },
  {
    "url": "assets/js/51.ede260be.js",
    "revision": "585514e300a60da9dde2df069e34928d"
  },
  {
    "url": "assets/js/52.8eff543e.js",
    "revision": "cefc1e142697875317e4d37fa4d12aae"
  },
  {
    "url": "assets/js/53.c7553d91.js",
    "revision": "752b9d38de8921108e06f0143fa8695d"
  },
  {
    "url": "assets/js/54.959a5e47.js",
    "revision": "afa9ec435d6d6e38cbf277b804e7b621"
  },
  {
    "url": "assets/js/55.69761532.js",
    "revision": "a79d687b4c4f765cea5d7df230d01a4c"
  },
  {
    "url": "assets/js/56.e39c4a02.js",
    "revision": "8dd3b1927754261111a26909fc156af1"
  },
  {
    "url": "assets/js/57.12368602.js",
    "revision": "ebdccdca08168d6b3a4d3105dc8cb541"
  },
  {
    "url": "assets/js/58.ee3a2925.js",
    "revision": "15825f2bed78562510658069e6b5f993"
  },
  {
    "url": "assets/js/59.db7ecd7f.js",
    "revision": "f36c10d3e741d0eb7d1d89e5a1989d1d"
  },
  {
    "url": "assets/js/6.6400e0e3.js",
    "revision": "9cb0e384ed847826d9991dfdaebd0cae"
  },
  {
    "url": "assets/js/60.0ca8b191.js",
    "revision": "2e11e6dc67a0595d68aafd23f3bef47b"
  },
  {
    "url": "assets/js/61.de1a34cd.js",
    "revision": "7d183eb18924b0499a8a9284a85eb09d"
  },
  {
    "url": "assets/js/62.dada056d.js",
    "revision": "c6e62aafb1df4a4a1915b03de28341bf"
  },
  {
    "url": "assets/js/63.9a2de471.js",
    "revision": "3bf99967453a52e91aa0bc17224e11db"
  },
  {
    "url": "assets/js/64.7e3af515.js",
    "revision": "37021b0cca246cccb2f1e7ee2ca75ff8"
  },
  {
    "url": "assets/js/65.ed1a240d.js",
    "revision": "3d502c64cb1b560f97a06e3af767dc73"
  },
  {
    "url": "assets/js/66.60dc53c5.js",
    "revision": "c52a2e051d4b62fc339fef423057802e"
  },
  {
    "url": "assets/js/67.756b66f5.js",
    "revision": "4b5fabc93755f6ef2350007bcb1d47f3"
  },
  {
    "url": "assets/js/68.6df6f4b0.js",
    "revision": "16a31524a8e8acad44b27b4f9c5f29e0"
  },
  {
    "url": "assets/js/69.ce426eb0.js",
    "revision": "738e61fef4af0351d84fcbf671eadcb1"
  },
  {
    "url": "assets/js/7.b43e2df1.js",
    "revision": "0554f9d8864ec2ba9b6725a238e3cf81"
  },
  {
    "url": "assets/js/70.18c88869.js",
    "revision": "8644e5878bf53c74561b9d0ca61b38b6"
  },
  {
    "url": "assets/js/71.f107a4fc.js",
    "revision": "f69be344a7210fda9d1c2c97ba90af2b"
  },
  {
    "url": "assets/js/72.c7b47378.js",
    "revision": "33e9ff16ba21c7f248882100e293f0bb"
  },
  {
    "url": "assets/js/73.2b4409db.js",
    "revision": "a53ec790fee15e7d49f598ed75696481"
  },
  {
    "url": "assets/js/74.c7adc88a.js",
    "revision": "743b4f65217a8784d338216bd0e0359c"
  },
  {
    "url": "assets/js/75.624d9671.js",
    "revision": "e08658922f2458edba943b75a959394f"
  },
  {
    "url": "assets/js/76.acc20976.js",
    "revision": "b97ccd60b5141586ce9917540be029ab"
  },
  {
    "url": "assets/js/77.b2a9ca03.js",
    "revision": "02bb645db2921d76cc138d232560986f"
  },
  {
    "url": "assets/js/78.47ec1fbd.js",
    "revision": "f619530dcc8f71c50aa4ddd9f2729792"
  },
  {
    "url": "assets/js/79.2ac9b08b.js",
    "revision": "7483cd7a13e77dfe8b5aa8c6df822731"
  },
  {
    "url": "assets/js/8.49c5213c.js",
    "revision": "f4e0b2bcb7ab32724efa470bae88153b"
  },
  {
    "url": "assets/js/80.39950fda.js",
    "revision": "734656be7d46eff344c31c2c559718e4"
  },
  {
    "url": "assets/js/81.2682a455.js",
    "revision": "76dc4262dc2b06a04bbd4b3430812789"
  },
  {
    "url": "assets/js/82.2751592a.js",
    "revision": "7107e73e0ee6c94fd62e52fb89997f67"
  },
  {
    "url": "assets/js/83.5149f135.js",
    "revision": "15eba28eb555809a31171604ed4381c6"
  },
  {
    "url": "assets/js/84.23ef4f23.js",
    "revision": "2f5e210aa5dfa7aa6b4f82c1e619e43b"
  },
  {
    "url": "assets/js/85.2270f2c6.js",
    "revision": "7d7d146bb1b113dc6e9a8a1602e2a831"
  },
  {
    "url": "assets/js/86.a20018e3.js",
    "revision": "325b5165baa6e74426fa864c77f56caf"
  },
  {
    "url": "assets/js/87.62df9412.js",
    "revision": "605044ccaa21abad86f58dc40b6dd321"
  },
  {
    "url": "assets/js/88.0a488943.js",
    "revision": "5b0879df070a00daabc049bd01e4be04"
  },
  {
    "url": "assets/js/89.cd073d8b.js",
    "revision": "c6bfb43185471c16a46f348c1269cd15"
  },
  {
    "url": "assets/js/9.f271619a.js",
    "revision": "eeaeb1a5bf63ff9356e9ab15acec4945"
  },
  {
    "url": "assets/js/90.bf5b70cc.js",
    "revision": "ecce0730a26e5b056dac0efbcb167e39"
  },
  {
    "url": "assets/js/91.313184e2.js",
    "revision": "a9cb7d664349bbe3ec9ad70041b7230d"
  },
  {
    "url": "assets/js/92.4f6a7ded.js",
    "revision": "4200503bb2c2ee06fc048b0638d3fd26"
  },
  {
    "url": "assets/js/93.25d3365a.js",
    "revision": "fd41c5b955d4263601cbe235b9991d28"
  },
  {
    "url": "assets/js/94.38ac9971.js",
    "revision": "9d4cc761a2b429353e92fe034765d9d1"
  },
  {
    "url": "assets/js/95.b552cea8.js",
    "revision": "edca481524ee53b05d553c3134a2deee"
  },
  {
    "url": "assets/js/96.55125488.js",
    "revision": "fb525921985d10df3ad6dc2085aff10c"
  },
  {
    "url": "assets/js/97.610e53f1.js",
    "revision": "d9f1b5963aa9cc77eaf85a6994d53362"
  },
  {
    "url": "assets/js/98.c7a19a42.js",
    "revision": "5b80090a83f7e2a30dc8b86eb2742c6e"
  },
  {
    "url": "assets/js/99.8b5ab92a.js",
    "revision": "b1752bbe92c54e58fc7f3eba1cccf3f4"
  },
  {
    "url": "assets/js/app.685ac49e.js",
    "revision": "f2fb666a0aa75b3a2a559d404aa088cf"
  },
  {
    "url": "assets/js/vendors~docsearch.8e8500d6.js",
    "revision": "ceef91c61f8b7c7d0927f55fad6131c2"
  },
  {
    "url": "changelog.html",
    "revision": "f269c34a805736fcf112f36ac9eec48e"
  },
  {
    "url": "guide/basic-configuration.html",
    "revision": "a28b5aaae1161cb43ff3a5443404a8fe"
  },
  {
    "url": "guide/cqhttp-guide.html",
    "revision": "328a226017978bbd6df49358175984c1"
  },
  {
    "url": "guide/creating-a-handler.html",
    "revision": "86c2d7848d9dc0aafb086c6c8f97083e"
  },
  {
    "url": "guide/creating-a-matcher.html",
    "revision": "c89ce8d3ba78868787b672c7ae33c09f"
  },
  {
    "url": "guide/creating-a-plugin.html",
    "revision": "ac45825f45043158baa58f4166cc824d"
  },
  {
    "url": "guide/creating-a-project.html",
    "revision": "76880fd5c2a88394c328e42072bfeac2"
  },
  {
    "url": "guide/ding-guide.html",
    "revision": "f1c52153c0a372b690cff0b6d8df9a35"
  },
  {
    "url": "guide/end-or-start.html",
    "revision": "c0eb83afd18f862bf73395c45ec7be7a"
  },
  {
    "url": "guide/feishu-guide.html",
    "revision": "e9a786cd7d4dbf7f608b81b2f40035b6"
  },
  {
    "url": "guide/getting-started.html",
    "revision": "acea5171877998cff1837c9d409abda7"
  },
  {
    "url": "guide/index.html",
    "revision": "e6424dc7d75e8a69f5f1af6aed5078f5"
  },
  {
    "url": "guide/installation.html",
    "revision": "a55ac4d48b38424776e8dc96ad0daba8"
  },
  {
    "url": "guide/loading-a-plugin.html",
    "revision": "3ded676574e068f5c378b6181a05765d"
  },
  {
    "url": "guide/mirai-guide.html",
    "revision": "f57540c9c1fe25fedc354005b6e6b653"
  },
  {
    "url": "icons/android-chrome-192x192.png",
    "revision": "36b48f1887823be77c6a7656435e3e07"
  },
  {
    "url": "icons/android-chrome-384x384.png",
    "revision": "e0dc7c6250bd5072e055287fc621290b"
  },
  {
    "url": "icons/apple-touch-icon-180x180.png",
    "revision": "b8d652dd0e29786cc95c37f8ddc238de"
  },
  {
    "url": "icons/favicon-16x16.png",
    "revision": "e6c309ee1ea59d3fb1ee0582c1a7f78d"
  },
  {
    "url": "icons/favicon-32x32.png",
    "revision": "d42193f7a38ef14edb19feef8e055edc"
  },
  {
    "url": "icons/mstile-150x150.png",
    "revision": "a76847a12740d7066f602a3e627ec8c3"
  },
  {
    "url": "icons/safari-pinned-tab.svg",
    "revision": "18f1a1363394632fa5fabf95875459ab"
  },
  {
    "url": "index.html",
    "revision": "20a54bc5c34c8fe3c573dc7b18d37e9c"
  },
  {
    "url": "logo.png",
    "revision": "2a63bac044dffd4d8b6c67f87e1c2a85"
  },
  {
    "url": "next/advanced/export-and-require.html",
    "revision": "c5c18686254a1b97123ffe8e6a10f190"
  },
  {
    "url": "next/advanced/index.html",
    "revision": "63168d3ffa1d9ed9933905477862599f"
  },
  {
    "url": "next/advanced/overloaded-handlers.html",
    "revision": "e3e4a40811b8a639f237399332c63ba3"
  },
  {
    "url": "next/advanced/permission.html",
    "revision": "ef4ada89be7c7d6b738394d70127f441"
  },
  {
    "url": "next/advanced/publish-plugin.html",
    "revision": "2914d16ba616f20ff3c9e4b703504a8b"
  },
  {
    "url": "next/advanced/runtime-hook.html",
    "revision": "3cd84a4881ff3d51c5fad0bf513b62b9"
  },
  {
    "url": "next/advanced/scheduler.html",
    "revision": "f9dfb97b6f47ba8c38ef7b067f5d6ab1"
  },
  {
    "url": "next/api/adapters/cqhttp.html",
    "revision": "b280298b43a8b6444ac2d71e07abe750"
  },
  {
    "url": "next/api/adapters/ding.html",
    "revision": "e8fda3374b761d3dcf47779aae785935"
  },
  {
    "url": "next/api/adapters/feishu.html",
    "revision": "c0ce4408010233751198115a85351f36"
  },
  {
    "url": "next/api/adapters/index.html",
    "revision": "26a1f335da8cf5d7d84acb5bdab9e2bf"
  },
  {
    "url": "next/api/adapters/mirai.html",
    "revision": "a09465e60c78746bcdfd0e6fef569c9a"
  },
  {
    "url": "next/api/config.html",
    "revision": "7c914dd7cfb43566d2b80247c80ac3b0"
  },
  {
    "url": "next/api/drivers/aiohttp.html",
    "revision": "9b0869591f2ede3f000d7ffcadde71b6"
  },
  {
    "url": "next/api/drivers/fastapi.html",
    "revision": "7ba7c21aa18ea182fd0759324b78c23c"
  },
  {
    "url": "next/api/drivers/index.html",
    "revision": "73f4929f62f9c4a35bd3cffb9ad45047"
  },
  {
    "url": "next/api/drivers/quart.html",
    "revision": "f6373dbf2c32b84989f82082ee95173c"
  },
  {
    "url": "next/api/exception.html",
    "revision": "1bcddcd9f2463e765034073c64c9d3a9"
  },
  {
    "url": "next/api/handler.html",
    "revision": "c9fdeb9247f9c95a484a57cbd97e79ee"
  },
  {
    "url": "next/api/index.html",
    "revision": "a1a45d2b5b57f88adf2f07b94d68fc53"
  },
  {
    "url": "next/api/log.html",
    "revision": "e4193681696eced1546115a023512fa9"
  },
  {
    "url": "next/api/matcher.html",
    "revision": "548fdf338fe8f4e6d66f091f2349c7e1"
  },
  {
    "url": "next/api/message.html",
    "revision": "eed2b0a1840be9c1c7ea708e793e2bbe"
  },
  {
    "url": "next/api/nonebot.html",
    "revision": "573098789f88ee3d5c4cde27ff50044c"
  },
  {
    "url": "next/api/permission.html",
    "revision": "fa447585cfed7e6a72f12928f5cac708"
  },
  {
    "url": "next/api/plugin.html",
    "revision": "2cc1f17c614f28f04e194f3b05e21fe6"
  },
  {
    "url": "next/api/rule.html",
    "revision": "c5bcb169892da867055886424c2c44f6"
  },
  {
    "url": "next/api/typing.html",
    "revision": "90a628d75c182ceb5bedfac22c57eff0"
  },
  {
    "url": "next/api/utils.html",
    "revision": "c1db2df7b5793c3e72997f0f034e3317"
  },
  {
    "url": "next/guide/basic-configuration.html",
    "revision": "b3d2303c46188fa38e8cc0c2141f2326"
  },
  {
    "url": "next/guide/cqhttp-guide.html",
    "revision": "84ea5716d0b58f941ac6e14b12d36288"
  },
  {
    "url": "next/guide/creating-a-handler.html",
    "revision": "0a758a1930e3c2ef093ba7fb3daace1f"
  },
  {
    "url": "next/guide/creating-a-matcher.html",
    "revision": "8182671e7112643ee0179b4cd53e02b8"
  },
  {
    "url": "next/guide/creating-a-plugin.html",
    "revision": "8003f3f882e11af1fdfb0a24d258bb8a"
  },
  {
    "url": "next/guide/creating-a-project.html",
    "revision": "73ed7f185fa01eb0a9326ae5958a471f"
  },
  {
    "url": "next/guide/ding-guide.html",
    "revision": "c841bb820576c664c594015b59ac20b3"
  },
  {
    "url": "next/guide/end-or-start.html",
    "revision": "09be782ded73f0af08c22ffeb22eb0de"
  },
  {
    "url": "next/guide/feishu-guide.html",
    "revision": "15de497879f4d586ea0ba00c3a081909"
  },
  {
    "url": "next/guide/getting-started.html",
    "revision": "d801115a52d1be63ca91ce7864a7ad6d"
  },
  {
    "url": "next/guide/index.html",
    "revision": "322c224da8e6bac04ef68f9177610f2d"
  },
  {
    "url": "next/guide/installation.html",
    "revision": "88f55068ac79f8883a069c178e9e9aad"
  },
  {
    "url": "next/guide/loading-a-plugin.html",
    "revision": "28d1098c6528ca5eafbfb321f9aa14d7"
  },
  {
    "url": "next/guide/mirai-guide.html",
    "revision": "e66613211b3dcfecbc0dac883a6b10c0"
  },
  {
    "url": "next/index.html",
    "revision": "fb9b2f861c38e823ed39b117e579fe65"
  },
  {
    "url": "store.html",
    "revision": "e7d2de06060866dc2890b33d4f66da8e"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
