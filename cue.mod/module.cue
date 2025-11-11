module: "github.com/cue-lang/cue-py"
language: {
	version: "v0.8.0"
}
deps: {
	"cue.dev/x/githubactions@v0": {
		v:       "v0.2.0"
		default: true
	}
	"github.com/cue-lang/tmp/internal/ci@v0": {
		v: "v0.0.10"
	}
}
