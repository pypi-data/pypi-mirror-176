from conan.api.model import UploadBundle
from conan.api.output import ConanOutput
from conan.api.subapi import api_method
from conan.api.conan_app import ConanApp
from conans.client.cmd.uploader import IntegrityChecker, PackagePreparator, UploadExecutor, \
    UploadUpstreamChecker
from conans.client.pkg_sign import PkgSignaturesPlugin
from conans.errors import ConanException


class UploadAPI:

    def __init__(self, conan_api):
        self.conan_api = conan_api

    @api_method
    def get_bundle(self, expression, package_query=None, only_recipe=False):
        ret = UploadBundle()
        if ":" in expression or package_query:
            # We are uploading the selected packages and the recipes belonging to that
            prefs = self.conan_api.search.package_revisions(expression, query=package_query)
            if not prefs:
                raise ConanException("There are no packages matching {}".format(expression))
            ret.add_prefs(prefs)
        else:
            # Upload the recipes and all the packages
            refs = self.conan_api.search.recipe_revisions(expression)
            if only_recipe:
                for ref in refs:
                    ret.add_ref(ref)
                return ret
            app = ConanApp(self.conan_api.cache_folder)
            for ref in refs:
                # Get all the prefs and all the prevs
                pkg_ids = app.cache.get_package_references(ref, only_latest_prev=False)
                if pkg_ids:
                    ret.add_prefs(pkg_ids)
                else:
                    ret.add_ref(ref)

        # This is necessary to upload_policy = "skip"
        app = ConanApp(self.conan_api.cache_folder)
        for recipe in ret.recipes:
            layout = app.cache.ref_layout(recipe.ref)
            conanfile_path = layout.conanfile()
            conanfile = app.loader.load_basic(conanfile_path)
            if conanfile.upload_policy == "skip":
                ConanOutput().info(f"{recipe.ref}: Skipping upload of binaries, "
                                   "because upload_policy='skip'")
                recipe.packages = []
        return ret

    @api_method
    def check_integrity(self, upload_data):
        """Check if the recipes and packages are corrupted (it will raise a ConanExcepcion)"""
        app = ConanApp(self.conan_api.cache_folder)
        checker = IntegrityChecker(app)
        checker.check(upload_data)

    @api_method
    def check_upstream(self, upload_bundle, remote, force=False):
        """Check if the artifacts are already in the specified remote, skipping them from
        the upload_bundle in that case"""
        app = ConanApp(self.conan_api.cache_folder)
        UploadUpstreamChecker(app).check(upload_bundle, remote, force)

    @api_method
    def prepare(self, upload_bundle, enabled_remotes):
        """Compress the recipes and packages and fill the upload_data objects
        with the complete information. It doesn't perform the upload nor checks upstream to see
        if the recipe is still there"""
        app = ConanApp(self.conan_api.cache_folder)
        preparator = PackagePreparator(app)
        preparator.prepare(upload_bundle, enabled_remotes)
        signer = PkgSignaturesPlugin(app.cache)
        # This might add files entries to upload_bundle with signatures
        signer.sign(upload_bundle)

    @api_method
    def upload_bundle(self, upload_bundle, remote):
        app = ConanApp(self.conan_api.cache_folder)
        app.remote_manager.check_credentials(remote)
        executor = UploadExecutor(app)
        executor.upload(upload_bundle, remote)
