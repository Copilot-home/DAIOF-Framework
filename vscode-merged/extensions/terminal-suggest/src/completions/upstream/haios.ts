const completionSpec: Fig.Spec = {
  name: "haios",
  description: "HyperAI OS Control CLI",
  subcommands: [
    {
      name: "think",
      description: "Trigger Socratic Reflection on an intent",
      args: {
        name: "intent",
        description: "The directive for HyperAI to evaluate",
      },
    },
    {
      name: "execute",
      description: "Evaluate and immediately execute a directive via DAIOF Bridge",
      args: {
        name: "directive",
        description: "The command to run through the Sovereign Mesh",
      },
    },
    {
      name: "audit",
      description: "Run DSS V3 Fresh Machine tests on the current topology",
      options: [
        {
          name: ["-f", "--force"],
          description: "Force clear node_modules before audit",
        },
      ],
    },
    {
      name: "status",
      description: "Check Symphony Control Center harmony score",
    }
  ],
};

export default completionSpec;
