# Extremely cursed flatpak nightly ci for snekstudio

## TLDR on usage

### Add Repo

```
$ flatpak remote-add snekstudio-nightly oci+https://lunarequest.github.io/snekstudio-flatpak-repo
```

### Install SnekStudio

```
$ flatpak install snekstudio-nightly com.snekstudio.Snekstudio
```


## How it works

~~I wish i could tell you~~. So reader you want cursed knowledge, knowing this will probably not make your life better, or worse but yeah its boring so like don't or something. This basically starts with the release workflow firing off because of a cron. The cron is set about an hour after the snekstudio github nighlty workflow runs. We then use jq and curl to get the urls of the latest binaries from the github repo. If this is the same as the urls stored in update.json we set the output newnightly to true. If it's false everything stops here. If there is an update, we commit this and push(this will not trigger a workflow run in push since update.json is a ignored path). We then move to the next job which downloads a static build of docker and uses it to register qemu binfmt runners so we can exectue arm64 code on amd64.

We then download the new binaries based on the new urls we've got. This is then used to to build the flatpaks using the `flatpak/flatpak-github-actions/flatpak-builder` action. While I tried building without I did not have any success.After this we bundle the flatpak build repos and upload them as release artifacts. The next job downloads these build repos and then uses these to create oci bundles. These oci bundles are pushed to [ghcr.io](https://ghcr.io) using skopeo. Once these are pushed we move to the next job which clones the repo and updates the repos folder with the image information for nightly and nightly-aarch64. On a push to main. It triggers the push workflow.

The push workflow then clones the repo on mistress and gh-pages. We then merge both the repo files into index/static on the gh-pages branch. If there are any changes we commit and push the changes to the gh-pages repo where it is then deployed. This effectively mean's our flatpak infra lives in github's container registry and we do not need any special hardware for this. In the future snekstudio stable should probably live in flathub but for now this should work 

